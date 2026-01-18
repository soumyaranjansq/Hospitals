from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory

from accounts.decorators import hospital_required
from .models import Hospital, Bill, BillDocument, Service, Scheme
from .forms import BillForm, BillDocumentForm


@login_required
@hospital_required
def hospital_dashboard(request):
    hospital = request.user.profile.hospital
    bills = Bill.objects.filter(hospital=hospital).order_by('-created_at')[:20]

    return render(request, 'hospitals/dashboard.html', {
        'hospital': hospital,
        'bills': bills,
    })


@login_required
@hospital_required
def submit_bill(request):
    hospital = request.user.profile.hospital

    DocumentFormSet = modelformset_factory(
        BillDocument,
        form=BillDocumentForm,
        extra=1,          # ✅ IMPORTANT
        can_delete=False
    )

    services = Service.objects.filter(is_active=True)

    if request.method == 'POST':
        bill_form = BillForm(request.POST)

        # ✅ MUST SET queryset on POST also
        bill_form.fields['scheme'].queryset = Scheme.objects.filter(is_active=True)

        formset = DocumentFormSet(
            request.POST,
            request.FILES,
            queryset=BillDocument.objects.none()
        )

        if bill_form.is_valid() and formset.is_valid():
            bill = bill_form.save(commit=False)
            bill.hospital = hospital
            bill.status = 'SUBMITTED'
            bill.save()

            for form in formset:
                if form.cleaned_data.get('file'):
                    doc = form.save(commit=False)
                    doc.bill = bill
                    doc.save()

            messages.success(request, 'Bill submitted successfully.')
            return redirect('hospitals:dashboard')

        # 🔴 TEMP DEBUG (REMOVE AFTER CONFIRM)
        print("❌ BillForm errors:", bill_form.errors)
        print("❌ Formset errors:", formset.errors)

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
    hospital = request.user.profile.hospital
    bills = Bill.objects.filter(hospital=hospital).order_by('-created_at')

    return render(request, 'hospitals/bill_list.html', {
        'hospital': hospital,
        'bills': bills,
    })


@login_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    documents = bill.documents.all()

    return render(request, 'hospitals/bill_detail.html', {
        'bill': bill,
        'documents': documents,
    })
