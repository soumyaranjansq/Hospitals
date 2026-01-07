from django.contrib import admin
from .models import Hospital, Service, Bill, LineItem, BillDocument

admin.site.register(Hospital)
admin.site.register(Service)
admin.site.register(Bill)
admin.site.register(LineItem)
admin.site.register(BillDocument)
