from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    """Hospital entity with tier classification."""
    
    TIER_CHOICES = (
        ('TIER1', 'Tier-1'),
        ('TIER2', 'Tier-2'),
    )
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Service(models.Model):
    """Medical service catalog with tier-based rates."""
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    base_rate_tier1 = models.DecimalField(max_digits=10, decimal_places=2)
    base_rate_tier2 = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Scheme(models.Model):
    """Reimbursement scheme (e.g., EHS, Pensioners)."""
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Bill(models.Model):
    """Medical bill submitted by hospital."""
    
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CLARIFICATION', 'Clarification Needed'),
    )
    
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='bills')
    scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT, related_name='bills', null=True, blank=True)
    patient_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, blank=True)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    bill_number = models.CharField(max_length=50)
    bill_date = models.DateField()
    gross_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    submission_date = models.DateTimeField(null=True, blank=True)
    tgnpdcl_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    gst_number = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.bill_number} - {self.hospital.name}"


class LineItem(models.Model):
    """Individual line items in a bill."""
    
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True)
    service_name = models.CharField(max_length=255)
    service_code = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.amount = self.rate * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.service_name} - ₹{self.amount}"


class BillDocument(models.Model):
    """Documents attached to a bill (stored in S3)."""
    
    DOC_TYPE_CHOICES = (
        ('ANNEXURE_C', 'Annexure-C'),
        ('ANNEXURE_D', 'Annexure-D'),
        ('INVOICE', 'Invoice'),
        ('PRESCRIPTION', 'Prescription'),
        ('DISCHARGE_SUMMARY', 'Discharge Summary'),
        ('LAB_REPORT', 'Lab Report'),
        ('OTHER', 'Other'),
    )
    
    bill = models.ForeignKey(Bill, related_name='documents', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True, help_text="Associated Billing Head")
    doc_type = models.CharField(max_length=50, choices=DOC_TYPE_CHOICES)
    file = models.FileField(upload_to='bill_documents/%Y/%m/')
    original_filename = models.CharField(max_length=255)
    is_mandatory = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.bill.bill_number}"
