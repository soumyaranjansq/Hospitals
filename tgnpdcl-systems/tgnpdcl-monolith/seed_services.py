from hospitals.models import Service

services_to_add = [
    ("Hospital Services", "HOSP_SERV"),
    ("Pharmacy / Drugs / Medicine Charges", "PHARMA_CHG"),
    ("Pharmacy / Drugs / Medicine Returns", "PHARMA_RET"),
    ("Intensive Care Units", "ICU"),
    ("Room Rent", "ROOM_RENT"),
    ("Investigations", "INVEST"),
    ("Invasive / Non-Invasive Procedures", "PROC_IV"),
    ("Surgery Charges", "SURG_CHG"),
    ("Procedure Charges", "PROC_CHG"),
    ("Packages", "PACKAGES"),
    ("Blood Bank", "BLOOD_BANK"),
    ("Disposables", "DISPOSABLES"),
    ("Consultation Charges", "CONSULT"),
    ("Implants / Medical Appliances", "IMPLANTS"),
    ("Medical Equipment", "MED_EQUIP"),
    ("Other Hospital Services", "OTHER_HOSP"),
]

for name, code in services_to_add:
    service, created = Service.objects.get_or_create(
        code=code,
        defaults={
            'name': name,
            'base_rate_tier1': 0.00,
            'base_rate_tier2': 0.00,
            'is_active': True
        }
    )
    if created:
        print(f"✅ Created service: {name} ({code})")
    else:
        # Update name if it's different
        if service.name != name:
            service.name = name
            service.save()
            print(f"🔄 Updated service: {name} ({code})")
        else:
            print(f"ℹ️ Service already exists: {name} ({code})")

print("\n✨ Seeding complete!")
