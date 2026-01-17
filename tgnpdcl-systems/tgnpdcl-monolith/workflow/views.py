from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import approver_required, role_required
from .models import SanctionRequest, ApprovalLog, WorkflowStep


@login_required
@approver_required
def approval_queue(request):
    """Show pending approvals assigned to the current user."""
    profile = request.user.profile
    role = profile.role
    
    # Find ALL steps that match this role
    steps = WorkflowStep.objects.filter(role_name=role)
    
    if not steps.exists():
        messages.warning(request, 'No workflow steps configured for your role.')
        return redirect('dashboard')
    
    # Show requests at ANY of these steps assigned to this user OR unassigned
    pending_requests = SanctionRequest.objects.filter(
        Q(assigned_to=request.user) | Q(assigned_to__isnull=True),
        current_step__in=steps,
        status__in=['PENDING', 'IN_PROGRESS']
    ).order_by('created_at')
    
    return render(request, 'workflow/approval_queue.html', {
        'step': steps.first(),
        'pending_requests': pending_requests,
    })


@login_required
@role_required('CUSTOMER_ADMIN')
def customer_admin_allocation(request):
    """Dashboard for Customer Admin to allocate tasks."""
    requests = SanctionRequest.objects.exclude(status__in=['APPROVED', 'REJECTED'])
    
    # Get all potential assignees (officers)
    assignees = User.objects.filter(profile__role__in=['JPO', 'APO', 'DPO', 'FA_CAO', 'DE', 'SE_CGM'])
    
    return render(request, 'workflow/task_allocation.html', {
        'requests': requests,
        'assignees': assignees,
    })


@login_required
@role_required('CUSTOMER_ADMIN')
def allocate_task(request, request_id):
    """View to handle task assignment."""
    if request.method == 'POST':
        sanction_request = get_object_or_404(SanctionRequest, id=request_id)
        user_id = request.POST.get('assignee_id')
        
        if user_id:
            assignee = get_object_or_404(User, id=user_id)
            sanction_request.assigned_to = assignee
            sanction_request.save()
            
            # Log the allocation
            ApprovalLog.objects.create(
                request=sanction_request,
                step=sanction_request.current_step,
                user=request.user,
                action='FORWARD', # Re-using FORWARD as a generic "moved to next step/person"
                comments=f"Task allocated to {assignee.get_full_name() or assignee.username} by Customer Admin."
            )
            
            messages.success(request, f'Task successfully allocated to {assignee.username}.')
        else:
            messages.error(request, 'No assignee selected.')
            
    return redirect('workflow:customer_admin_allocation')


@login_required
@approver_required
def request_detail(request, request_id):
    """View sanction request details."""
    sanction_request = get_object_or_404(SanctionRequest, id=request_id)
    logs = sanction_request.logs.all()
    
    # Get bill documents
    try:
        bill_documents = sanction_request.bill.documents.all()
    except:
        bill_documents = []
    
    return render(request, 'workflow/request_detail.html', {
        'sanction_request': sanction_request,
        'logs': logs,
        'bill_documents': bill_documents,
    })


@login_required
@approver_required
def process_request(request, request_id):
    """Process (approve/reject/forward) a sanction request."""
    sanction_request = get_object_or_404(SanctionRequest, id=request_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comments = request.POST.get('comments', '')
        amount = request.POST.get('approved_amount')
        
        # Create approval log
        ApprovalLog.objects.create(
            request=sanction_request,
            step=sanction_request.current_step,
            user=request.user,
            action=action,
            comments=comments,
            approved_amount_at_stage=amount if amount else None,
        )
        
        # Update request and bill status based on action
        if action == 'APPROVE':
            sanction_request.status = 'APPROVED'
            sanction_request.sanctioned_amount = amount
            # Update the linked bill as well
            sanction_request.bill.status = 'APPROVED'
            sanction_request.bill.save()
            messages.success(request, 'Request approved successfully.')
        elif action == 'REJECT':
            # Actual rejection (Step 6 and 7)
            sanction_request.status = 'REJECTED'
            sanction_request.bill.status = 'REJECTED'
            sanction_request.bill.save()
            messages.warning(request, 'Request rejected.')
        elif action in ['FORWARD', 'REJECT_RECOMMENDED']:
            # Move to next step
            next_step = WorkflowStep.objects.filter(
                order__gt=sanction_request.current_step.order
            ).first()
            if next_step:
                sanction_request.current_step = next_step
                sanction_request.status = 'IN_PROGRESS'
                sanction_request.assigned_to = None # Clear for re-allocation at next stage
                # Update bill to Under Review if it wasn't already
                if sanction_request.bill.status != 'UNDER_REVIEW':
                    sanction_request.bill.status = 'UNDER_REVIEW'
                    sanction_request.bill.save()
                
                msg = f'Request forwarded to {next_step.name}.'
                if action == 'REJECT_RECOMMENDED':
                    msg = f'Request forwarded to {next_step.name} with recommendation for rejection.'
                messages.success(request, msg)
            else:
                messages.error(request, 'No next step available. Please use "Approve Final" or "Reject".')
        elif action == 'CLARIFY':
            sanction_request.status = 'CLARIFICATION'
            # Update the linked bill as well
            sanction_request.bill.status = 'CLARIFICATION'
            sanction_request.bill.save()
            messages.info(request, 'Clarification requested from hospital.')
        
        sanction_request.save()
        return redirect('workflow:approval_queue')
    
    return redirect('workflow:request_detail', request_id=request_id)
