from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView
from rest_framework import viewsets
from .models import Hospital, Bill
from .serializers import HospitalSerializer, BillSerializer
from .forms import BillForm
from django.urls import reverse_lazy

# DRF Viewsets
class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

# Frontend Views
class BillListView(ListView):
    model = Bill
    template_name = 'hospitals/bill_list.html'
    context_object_name = 'bills'
    ordering = ['-submission_date']

    def get_queryset(self):
        # Determine the status to filter by from GET params or default to showing all
        status = self.request.GET.get('status')
        queryset = super().get_queryset()
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class BillCreateView(CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'hospitals/bill_form.html'
    success_url = reverse_lazy('bill_list')

    def form_valid(self, form):
        # Set default status or perform other logic
        form.instance.status = 'SUBMITTED'
        return super().form_valid(form)
