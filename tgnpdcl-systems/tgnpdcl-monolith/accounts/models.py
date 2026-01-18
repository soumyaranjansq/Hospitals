# # accounts/models.py 
# from django.db import models
# from django.contrib.auth.models import User


# class UserProfile(models.Model):
#     """Extended user profile with role-based access."""
    
#     ROLE_CHOICES = (
#         ('HOSPITAL', 'Hospital Admin'),
#         ('JPO', 'Junior Personnel Officer'),
#         ('APO', 'Assistant Personnel Officer'),
#         ('DPO', 'Deputy Personnel Officer'),
#         ('FA_CAO', 'Financial Advisor & CAO'),
#         ('DE', 'Deputy Engineer'),
#         ('SE_CGM', 'Senior Engineer / CGM'),
#         ('CUSTOMER_ADMIN', 'Customer Admin'),
#     )
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     designation = models.CharField(max_length=100, blank=True)
#     department = models.CharField(max_length=100, blank=True)
#     phone = models.CharField(max_length=15, blank=True)
    
#     # For Hospital role - link to hospital
#     hospital = models.ForeignKey(
#         'hospitals.Hospital',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='users'
#     )
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = 'User Profile'
#         verbose_name_plural = 'User Profiles'
    
#     def __str__(self):
#         return f"{self.user.username} ({self.get_role_display()})"
    
#     @property
#     def is_hospital_user(self):
#         return self.role == 'HOSPITAL'
    
#     @property
#     def is_approver(self):
#         return self.role in ['JPO', 'APO', 'DPO', 'FA_CAO', 'DE', 'SE_CGM']
    
#     @property
#     def can_final_approve(self):
#         return self.role == 'SE_CGM'




# accounts/models.py
# TGNPDCL Medical Bill Reimbursement System
# Accounts & Role Management Models

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    """
    Extended user profile with strict role-based access.
    Hospital users are linked to a Hospital.
    All other users operate via workflow, not hospital mapping.
    """

    ROLE_CHOICES = (
        ('HOSPITAL', 'Hospital Admin'),
        ('JPO', 'Junior Personnel Officer'),
        ('APO', 'Assistant Personnel Officer'),
        ('DPO', 'Deputy Personnel Officer'),
        ('FA_CAO', 'Financial Advisor & CAO'),
        ('DE', 'Deputy Engineer'),
        ('SE_CGM', 'Senior Engineer / CGM'),
        ('DIRECTOR', 'Director / Final Authority'),
        ('CUSTOMER_ADMIN', 'Customer Admin'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    # Only for Hospital role
    hospital = models.ForeignKey(
        'hospitals.Hospital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    # -----------------------------
    # Validation Rules
    # -----------------------------
    def clean(self):
        """
        Enforce role-to-hospital rules:
        - Hospital users MUST have hospital assigned
        - Non-hospital users MUST NOT have hospital assigned
        """
        if self.role == 'HOSPITAL' and not self.hospital:
            raise ValidationError({
                'hospital': 'Hospital must be assigned for Hospital users.'
            })

        if self.role != 'HOSPITAL' and self.hospital:
            raise ValidationError({
                'hospital': 'Only Hospital users can be linked to a hospital.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # -----------------------------
    # Convenience Properties
    # -----------------------------
    @property
    def is_hospital_user(self):
        return self.role == 'HOSPITAL'

    @property
    def is_approver(self):
        """
        Any role involved in approval workflow
        """
        return self.role in [
            'JPO', 'APO', 'DPO', 'FA_CAO', 'DE', 'SE_CGM', 'DIRECTOR'
        ]

    @property
    def can_final_approve(self):
        """
        Final sanction authority roles
        """
        return self.role in ['SE_CGM', 'DIRECTOR']

    @property
    def is_admin(self):
        """
        System-level admin (not workflow approver)
        """
        return self.role == 'CUSTOMER_ADMIN'
