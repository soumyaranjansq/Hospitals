from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    TIER_CHOICES = (
        ('TIER1', 'Tier-1'),
        ('TIER2', 'Tier-2'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Service(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    base_rate_tier1 = models.DecimalField(max_digits=10, decimal_places=2)
    base_rate_tier2 = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Bill(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT)
    patient_name = models.CharField(max_length=255)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    bill_number = models.CharField(max_length=50)
    bill_date = models.DateField()
    gross_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    submission_date = models.DateTimeField(null=True, blank=True)
    tgnpdcl_id = models.CharField(max_length=50, null=True, blank=True) # Unique ID from HO
    
    # Annexure-D Header Data (Simplified)
    gst_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.bill_number} - {self.hospital.name}"

class LineItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255) # Can be custom or from Service
    service_code = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=2) # Rate * Qty
    document_url = models.URLField(blank=True) # Link to document service
    
    def save(self, *args, **kwargs):
        self.amount = self.rate * self.quantity
        super().save(*args, **kwargs)

class BillDocument(models.Model):
    """
    For Annexure-C documents (Submission level or extra docs).
    Line item docs are handled in LineItem or here with a generic relation.
    Keeping it simple: Bill level docs.
    """
    bill = models.ForeignKey(Bill, related_name='documents', on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=50) # e.g., 'Annexure-C', 'Invoice'
    file_url = models.URLField()
    is_mandatory = models.BooleanField(default=False)
