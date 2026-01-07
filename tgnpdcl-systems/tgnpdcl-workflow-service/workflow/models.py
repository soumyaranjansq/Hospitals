from django.db import models
from django.contrib.auth.models import User

class WorkflowStep(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(unique=True) # 1 to 7
    role_name = models.CharField(max_length=100) # e.g., "Asst./JPO"
    can_reject = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.order}. {self.name}"

class SanctionLimit(models.Model):
    """
    Limits for auto-validation.
    E.g. category='EMPLOYEE', type='MINOR', limit=1000000
    """
    CATEGORY_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('PENSIONER', 'Pensioner'),
        ('FAMILY_PENSIONER', 'Family Pensioner'),
        ('ARTISAN', 'Artisan'),
    )
    TYPE_CHOICES = (
        ('MINOR', 'Minor'),
        ('MAJOR', 'Major'),
        ('SELF_FUNDING', 'Self Funding'),
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    limit_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.category} - {self.limit_type}: {self.amount}"

class SanctionRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CLARIFICATION', 'Clarification Needed'),
    )
    
    bill_id = models.CharField(max_length=50, unique=True) # From Hospital Service
    hospital_name = models.CharField(max_length=255)
    patient_name = models.CharField(max_length=255)
    
    # Financials
    claimed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    sanctioned_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    current_step = models.ForeignKey(WorkflowStep, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Validation flags
    is_limit_exceeded = models.BooleanField(default=False)

class ApprovalLog(models.Model):
    ACTION_CHOICES = (
        ('FORWARD', 'Forward'),
        ('REJECT', 'Reject'),
        ('APPROVE', 'Approve (Final)'),
        ('CLARIFY', 'Seek Clarification'),
    )
    
    request = models.ForeignKey(SanctionRequest, related_name='logs', on_delete=models.CASCADE)
    step = models.ForeignKey(WorkflowStep, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT) # The officer
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    comments = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Each level can edit amounts, so we capture snapshots
    approved_amount_at_stage = models.DecimalField(max_digits=12, decimal_places=2, null=True)
