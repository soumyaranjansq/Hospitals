# Script to create test users for all 7 roles
from django.contrib.auth.models import User
from accounts.models import UserProfile
from hospitals.models import Hospital
from workflow.models import WorkflowStep, SanctionLimit

print("Creating test data...")

# Create Workflow Steps
workflow_steps = [
    (1, 'JPO Review', 'JPO'),
    (2, 'APO Review', 'APO'),
    (3, 'DPO Review', 'DPO'),
    (4, 'FA & CAO Review', 'FA_CAO'),
    (5, 'DE Technical Review', 'DE'),
    (6, 'SE Final Review', 'SE_CGM'),
    (7, 'CGM Approval', 'SE_CGM'),
]

for order, name, role in workflow_steps:
    WorkflowStep.objects.get_or_create(
        order=order,
        defaults={'name': name, 'role_name': role}
    )
print("✅ Workflow Steps initialized")

# Create a hospital first
hospital, created = Hospital.objects.get_or_create(
    code="TH001",
    defaults={
        'name': "Test Hospital",
        'tier': "TIER1",
        'address': "123 Test Street, Test City"
    }
)
print(f"✅ Hospital: {hospital.name}")

# Create users for all 7 roles
roles = [
    ('hospital1', 'Hospital', 'Admin', 'HOSPITAL', 'Hospital Administrator', hospital),
    ('jpo1', 'JPO', 'Officer', 'JPO', 'Junior Personnel Officer', None),
    ('apo1', 'APO', 'Officer', 'APO', 'Assistant Personnel Officer', None),
    ('dpo1', 'DPO', 'Officer', 'DPO', 'Deputy Personnel Officer', None),
    ('facao1', 'FA', 'CAO', 'FA_CAO', 'Financial Advisor & CAO', None),
    ('de1', 'Deputy', 'Engineer', 'DE', 'Deputy Engineer', None),
    ('secgm1', 'Senior', 'Engineer', 'SE_CGM', 'Senior Engineer / CGM', None),
    ('customeradmin1', 'Customer', 'Admin', 'CUSTOMER_ADMIN', 'TGNPDCL System Administrator', None),
]

for username, first_name, last_name, role, designation, hosp in roles:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@tgnpdcl.com',
            'first_name': first_name,
            'last_name': last_name,
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'role': role,
            'designation': designation,
            'hospital': hosp
        }
    )
    print(f"✅ {username} ({designation})")

print("\n🎉 All test users created!")
print("\nLogin credentials:")
print("Username: hospital1, jpo1, apo1, dpo1, facao1, de1, secgm1, customeradmin1")
print("Password: password123")
print("\nVisit: http://localhost:8000")
