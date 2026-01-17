# from django import forms
# from .models import Bill, BillDocument

# class BillForm(forms.ModelForm):
#     class Meta:
#         model = Bill
#         fields = [
#             'scheme', 'patient_name', 'employee_id', 'admission_date', 
#             'discharge_date', 'bill_number', 'bill_date', 
#             'gross_total', 'gst_number'
#         ]
#         widgets = {
#             'scheme': forms.Select(attrs={'class': 'form-control'}),
#             'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'discharge_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'bill_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
#             'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TGNPDCL Employee ID'}),
#             'bill_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number'}),
#             'gross_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
#             'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
#         }

# class BillDocumentForm(forms.ModelForm):
#     class Meta:
#         model = BillDocument
#         fields = ['service', 'doc_type', 'file']
#         widgets = {
#             'service': forms.Select(attrs={'class': 'form-control'}),
#             'doc_type': forms.Select(attrs={'class': 'form-control'}),
#             'file': forms.FileInput(attrs={'class': 'form-control'}),
#         }



from django import forms
from .models import Bill, BillDocument


class BillForm(forms.ModelForm):
    """
    Hospital – Create and Submit Medical Claim
    (As per Annexure-D of requirements)
    """

    class Meta:
        model = Bill
        fields = [
            'scheme',
            'patient_name',
            'designation',
            'employee_id',
            'employee_type',
            'relationship',
            'credit_card_number',
            'ip_number',
            'mobile_number',
            'age',
            'sex',
            'disease_details',
            'admission_date',
            'discharge_date',
        ]

        widgets = {
            'scheme': forms.Select(attrs={'class': 'form-control'}),

            'patient_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Patient Name'}
            ),
            'designation': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Designation'}
            ),
            'employee_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Employee ID'}
            ),

            'employee_type': forms.Select(attrs={'class': 'form-control'}),
            'relationship': forms.Select(attrs={'class': 'form-control'}),

            'credit_card_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'CC Card Number'}
            ),
            'ip_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'IP Number'}
            ),

            'mobile_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}
            ),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(
                choices=[('Male', 'Male'), ('Female', 'Female')],
                attrs={'class': 'form-control'}
            ),

            'disease_details': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),

            'admission_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'discharge_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }


class BillDocumentForm(forms.ModelForm):
    """
    Annexure-C – Upload Mandatory / Optional Documents
    """

    class Meta:
        model = BillDocument
        fields = [
            'document_type',
            'file',
        ]

        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
