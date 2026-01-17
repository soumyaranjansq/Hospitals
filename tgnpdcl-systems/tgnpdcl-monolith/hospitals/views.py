from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory

from accounts.decorators import role_required, hospital_required
from .models import Hospital, Bill, BillDocument, Service, Scheme
from .forms import BillForm, BillDocumentForm
from workflow.models import SanctionRequest, WorkflowStep


@login_required
@hospital_required
def hospital_dashboard(request):
    """Dashboard for hospital users."""
    try:
        hospital = request.user.profile.hospital
    except AttributeError:
        messages.error(request, 'No hospital assigned to your account.')
        return redirect('dashboard')
    
    bills = Bill.objects.filter(hospital=hospital).order_by('-created_at')[:20]
    
    return render(request, 'hospitals/dashboard.html', {
        'hospital': hospital,
        'bills': bills,
    })


@login_required
@hospital_required
def submit_bill(request):
    """View to handle new bill submission with documents."""
    hospital = request.user.profile.hospital
    
    # Create a formset for multiple document uploads
    DocumentFormSet = modelformset_factory(
        BillDocument, 
        form=BillDocumentForm, 
        extra=0, # Start with 0, JS will add rows
        can_delete=False
    )
    
    services = Service.objects.filter(is_active=True)
    
    if request.method == 'POST':
        bill_form = BillForm(request.POST)
        formset = DocumentFormSet(request.POST, request.FILES, queryset=BillDocument.objects.none())
        
        if bill_form.is_valid() and formset.is_valid():
            bill = bill_form.save(commit=False)
            bill.hospital = hospital
            bill.created_by = request.user
            bill.status = 'SUBMITTED'
            bill.save()
            
            # Save documents
            for form in formset:
                if form.cleaned_data.get('file'):
                    doc = form.save(commit=False)
                    doc.bill = bill
                    doc.original_filename = doc.file.name
                    doc.save()
            
            # Create SanctionRequest to enter workflow
            first_step = WorkflowStep.objects.order_by('order').first()
            SanctionRequest.objects.create(
                bill=bill,
                hospital_name=hospital.name,
                patient_name=bill.patient_name,
                claimed_amount=bill.gross_total,
                current_step=first_step,
                status='PENDING'
            )
            
            messages.success(request, 'Bill submitted successfully and entered the approval workflow!')
            return redirect('hospitals:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        bill_form = BillForm()
        bill_form.fields['scheme'].queryset = Scheme.objects.filter(is_active=True)
        formset = DocumentFormSet(queryset=BillDocument.objects.none())
        
    return render(request, 'hospitals/submit_bill.html', {
        'bill_form': bill_form,
        'formset': formset,
        'services': services,
    })


@login_required
@hospital_required
def bill_list(request):
    """List all bills for the hospital."""
    try:
        hospital = request.user.profile.hospital
    except AttributeError:
        messages.error(request, 'No hospital assigned to your account.')
        return redirect('dashboard')
    
    bills = Bill.objects.filter(hospital=hospital).order_by('-created_at')
    
    return render(request, 'hospitals/bill_list.html', {
        'hospital': hospital,
        'bills': bills,
    })


@login_required
def bill_detail(request, bill_id):
    """View bill details with documents."""
    bill = get_object_or_404(Bill, id=bill_id)
    
    # Check access permissions
    profile = request.user.profile
    if profile.role == 'HOSPITAL':
        if profile.hospital != bill.hospital:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
    
    documents = bill.documents.all()
    
    return render(request, 'hospitals/bill_detail.html', {
        'bill': bill,
        'documents': documents,
    })
