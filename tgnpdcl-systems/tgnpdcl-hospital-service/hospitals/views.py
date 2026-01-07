from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Bill, LineItem, Hospital
from .serializers import BillSerializer, LineItemSerializer, HospitalSerializer

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show bills for the logged-in hospital
        if hasattr(self.request.user, 'hospital'):
            return Bill.objects.filter(hospital=self.request.user.hospital)
        return Bill.objects.none()

    def perform_create(self, serializer):
        # Auto-assign the hospital from the logged-in user
        if hasattr(self.request.user, 'hospital'):
            serializer.save(hospital=self.request.user.hospital)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        bill = self.get_object()
        if bill.status != 'DRAFT':
            return Response({'error': 'Only draft bills can be submitted'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Here we would trigger validation and workflow start
        # For now just update status
        from django.utils import timezone
        bill.status = 'SUBMITTED'
        bill.submission_date = timezone.now()
        bill.save()
        return Response({'status': 'Bill submitted successfully'})

class LineItemViewSet(viewsets.ModelViewSet):
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'hospital'):
            return LineItem.objects.filter(bill__hospital=self.request.user.hospital)
        return LineItem.objects.none()
