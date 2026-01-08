from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['hospital', 'bill_number', 'patient_name', 'admission_date', 
                  'discharge_date', 'bill_date', 'gross_total']
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bill_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'bill_number': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gross_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }
