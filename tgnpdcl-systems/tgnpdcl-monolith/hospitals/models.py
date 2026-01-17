# from django.db import models
# from django.contrib.auth.models import User


# class Hospital(models.Model):
#     """Hospital entity with tier classification."""
    
#     TIER_CHOICES = (
#         ('TIER1', 'Tier-1'),
#         ('TIER2', 'Tier-2'),
#     )
    
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=50, unique=True)
#     tier = models.CharField(max_length=10, choices=TIER_CHOICES)
#     address = models.TextField()
#     phone = models.CharField(max_length=15, blank=True)
#     email = models.EmailField(blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['name']
    
#     def __str__(self):
#         return f"{self.name} ({self.code})"


# class Service(models.Model):
#     """Medical service catalog with tier-based rates."""
    
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=50, unique=True)
#     base_rate_tier1 = models.DecimalField(max_digits=10, decimal_places=2)
#     base_rate_tier2 = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active = models.BooleanField(default=True)
    
#     class Meta:
#         ordering = ['name']
    
#     def __str__(self):
#         return f"{self.name} ({self.code})"


# class Scheme(models.Model):
#     """Reimbursement scheme (e.g., EHS, Pensioners)."""
    
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=50, unique=True)
#     description = models.TextField(blank=True)
#     is_active = models.BooleanField(default=True)
    
#     class Meta:
#         ordering = ['name']
        
#     def __str__(self):
#         return self.name


# class Bill(models.Model):
#     """Medical bill submitted by hospital."""
    
#     STATUS_CHOICES = (
#         ('DRAFT', 'Draft'),
#         ('SUBMITTED', 'Submitted'),
#         ('UNDER_REVIEW', 'Under Review'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#         ('CLARIFICATION', 'Clarification Needed'),
#     )
    
#     hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='bills')
#     scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT, related_name='bills', null=True, blank=True)
#     patient_name = models.CharField(max_length=255)
#     employee_id = models.CharField(max_length=50, blank=True)
#     admission_date = models.DateField()
#     discharge_date = models.DateField()
#     bill_number = models.CharField(max_length=50)
#     bill_date = models.DateField()
#     gross_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
#     submission_date = models.DateTimeField(null=True, blank=True)
#     tgnpdcl_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
#     gst_number = models.CharField(max_length=50, blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    
#     class Meta:
#         ordering = ['-created_at']
    
#     def __str__(self):
#         return f"{self.bill_number} - {self.hospital.name}"


# class LineItem(models.Model):
#     """Individual line items in a bill."""
    
#     bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True)
#     service_name = models.CharField(max_length=255)
#     service_code = models.CharField(max_length=50, blank=True)
#     description = models.TextField(blank=True)
#     rate = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.IntegerField(default=1)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
    
#     def save(self, *args, **kwargs):
#         self.amount = self.rate * self.quantity
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return f"{self.service_name} - ₹{self.amount}"


# class BillDocument(models.Model):
#     """Documents attached to a bill (stored in S3)."""
    
#     DOC_TYPE_CHOICES = (
#         ('ANNEXURE_C', 'Annexure-C'),
#         ('ANNEXURE_D', 'Annexure-D'),
#         ('INVOICE', 'Invoice'),
#         ('PRESCRIPTION', 'Prescription'),
#         ('DISCHARGE_SUMMARY', 'Discharge Summary'),
#         ('LAB_REPORT', 'Lab Report'),
#         ('OTHER', 'Other'),
#     )
    
#     bill = models.ForeignKey(Bill, related_name='documents', on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True, help_text="Associated Billing Head")
#     doc_type = models.CharField(max_length=50, choices=DOC_TYPE_CHOICES)
#     file = models.FileField(upload_to='bill_documents/%Y/%m/')
#     original_filename = models.CharField(max_length=255)
#     is_mandatory = models.BooleanField(default=False)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.get_doc_type_display()} - {self.bill.bill_number}"



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Hospital(models.Model):

    TIER_CHOICES = (
        ('TIER1', 'Tier-I'),
        ('TIER2', 'Tier-II'),
        ('TIER3', 'Tier-III'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='hospital_profile',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)

    district = models.CharField(max_length=100)
    address = models.TextField()

    pan_number = models.CharField(max_length=20, blank=True)
    gst_number = models.CharField(max_length=30, blank=True)
    cin_number = models.CharField(max_length=30, blank=True)

    valid_upto = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Service(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Scheme(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Bill(models.Model):

    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('IN_PROCESS', 'In Process'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    EMPLOYEE_TYPE_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('PENSIONER', 'Pensioner'),
        ('FAMILY_PENSIONER', 'Family Pensioner'),
        ('ARTISAN', 'Artisan'),
    )

    RELATIONSHIP_CHOICES = (
        ('SELF', 'Self'),
        ('DEPENDENT', 'Dependent'),
    )

    claim_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.PROTECT,
        related_name='claims'
    )

    scheme = models.ForeignKey(
        Scheme,
        on_delete=models.PROTECT,
        related_name='claims'
    )

    patient_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)

    employee_type = models.CharField(
        max_length=30,
        choices=EMPLOYEE_TYPE_CHOICES
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES
    )

    credit_card_number = models.CharField(max_length=50)
    ip_number = models.CharField(max_length=50)

    mobile_number = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10)

    disease_details = models.TextField()

    admission_date = models.DateField()
    discharge_date = models.DateField()

    gross_claimed_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    gross_approved_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    submitted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def submit_claim(self):
        self.status = 'SUBMITTED'
        self.submitted_at = timezone.now()
        self.save(update_fields=['status', 'submitted_at'])

    def __str__(self):
        return f"Claim {self.claim_id}"


class LineItem(models.Model):

    bill = models.ForeignKey(
        Bill,
        related_name='line_items',
        on_delete=models.CASCADE
    )

    service = models.ForeignKey(
        Service,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    hospital_service_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    claimed_rate = models.DecimalField(max_digits=10, decimal_places=2)
    claimed_quantity = models.PositiveIntegerField()
    claimed_amount = models.DecimalField(max_digits=12, decimal_places=2)

    approved_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    approved_quantity = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    comments = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.claimed_amount = self.claimed_rate * self.claimed_quantity
        if self.approved_rate is not None and self.approved_quantity is not None:
            self.approved_amount = self.approved_rate * self.approved_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.hospital_service_name


class BillDocument(models.Model):

    DOCUMENT_TYPE_CHOICES = (
        ('ID_CARD', 'Employee / Pensioner / Artisan ID Card'),
        ('CC_CARD', 'Approved CC Card'),
        ('FINAL_BILL', 'Final Hospital Bill'),
        ('DETAIL_BILL', 'Detailed Hospital Bill'),
        ('PHARMACY', 'Pharmacy Bill'),
        ('INVOICE', 'Invoice'),
        ('DISCHARGE', 'Discharge Summary'),
        ('OTHER', 'Other'),
    )

    bill = models.ForeignKey(
        Bill,
        related_name='documents',
        on_delete=models.CASCADE
    )

    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='medical_bills/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.bill.claim_id}"


class WorkflowHistory(models.Model):

    ACTION_CHOICES = (
        ('FORWARDED', 'Forwarded'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    bill = models.ForeignKey(
        Bill,
        related_name='workflow_history',
        on_delete=models.CASCADE
    )

    action_by = models.ForeignKey(User, on_delete=models.PROTECT)
    role = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    remarks = models.TextField(blank=True)
    action_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill.claim_id} - {self.action}"


class SanctionOrder(models.Model):

    bill = models.OneToOneField(
        Bill,
        on_delete=models.CASCADE,
        related_name='sanction_order'
    )

    order_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateField(auto_now_add=True)
    sanctioned_amount = models.DecimalField(max_digits=14, decimal_places=2)

    pdf_file = models.FileField(upload_to='sanction_orders/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sanction Order {self.order_number}"


    bill = models.OneToOneField(
        Bill,
        on_delete=models.CASCADE,
        related_name='sanction_order'
    )

    order_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateField(auto_now_add=True)

    sanctioned_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    pdf_file = models.FileField(upload_to='sanction_orders/')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Sanction Order {self.order_number}"