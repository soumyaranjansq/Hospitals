from django import forms
from .models import Bill, BillDocument

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            'scheme', 'patient_name', 'employee_id', 'admission_date', 
            'discharge_date', 'bill_number', 'bill_date', 
            'gross_total', 'gst_number'
        ]
        widgets = {
            'scheme': forms.Select(attrs={'class': 'form-control'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bill_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TGNPDCL Employee ID'}),
            'bill_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number'}),
            'gross_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
        }

class BillDocumentForm(forms.ModelForm):
    class Meta:
        model = BillDocument
        fields = ['service', 'doc_type', 'file']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'doc_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
