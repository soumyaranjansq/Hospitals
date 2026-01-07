from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import SanctionRequest, ApprovalLog, WorkflowStep, SanctionLimit
from .serializers import SanctionRequestSerializer, ApprovalLogSerializer

class SanctionRequestViewSet(viewsets.ModelViewSet):
    queryset = SanctionRequest.objects.all()
    serializer_class = SanctionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # When created (e.g. from Hospital Service webhook), set to first step
        first_step = WorkflowStep.objects.order_by('order').first()
        serializer.save(current_step=first_step)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """
        Handle Forward, Reject, Approve actions.
        Payload: {
            "action": "FORWARD" | "REJECT" | "APPROVE",
            "comments": "...",
            "approved_amount": 1000.00 (optional override)
        }
        """
        sanction_req = self.get_object()
        action_type = request.data.get('action')
        comments = request.data.get('comments', '')
        approved_amount = request.data.get('approved_amount')
        
        user = request.user
        current_step = sanction_req.current_step
        
        # TODO: Check if user belongs to the current_step role (simple check skipped for prototype)
        
        if approved_amount:
            sanction_req.sanctioned_amount = approved_amount
            # Run Limit Check
            # Assuming we know category/type from somewhere (maybe patient metadata passed in req)
            # check_limits(sanction_req) # implementation detail
        
        if action_type == 'FORWARD':
            next_step = WorkflowStep.objects.filter(order__gt=current_step.order).order_by('order').first()
            if not next_step:
                 # If no next step, maybe it should have been APPROVED?
                 return Response({'error': 'No next step found. Use APPROVE if final.'}, status=400)
            
            sanction_req.current_step = next_step
            sanction_req.save()
            
        elif action_type == 'REJECT':
            # Validation: Only Jt Secy or Director can reject
            if not current_step.can_reject:
                return Response({'error': 'Current level does not have rejection authority'}, status=403)
            
            sanction_req.status = 'REJECTED'
            sanction_req.save()
            
        elif action_type == 'APPROVE':
            # Validation: Only final step?
            # Prompt says "Sanction Order" comes after Director.
            sanction_req.status = 'APPROVED'
            sanction_req.save()
            # Trigger Sanction Order Generation (via Notification Service or Document Service)
            
        # Log the action
        ApprovalLog.objects.create(
            request=sanction_req,
            step=current_step,
            user=user,
            action=action_type,
            comments=comments,
            approved_amount_at_stage=sanction_req.sanctioned_amount
        )
        
        return Response({'status': 'Processed', 'new_status': sanction_req.status})
