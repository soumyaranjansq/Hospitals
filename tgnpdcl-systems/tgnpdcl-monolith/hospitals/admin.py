from django.contrib import admin
from .models import Hospital, Service, Bill, LineItem, BillDocument


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'tier', 'is_active', 'created_at')
    list_filter = ('tier', 'is_active')
    search_fields = ('name', 'code')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'base_rate_tier1', 'base_rate_tier2', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 0


class BillDocumentInline(admin.TabularInline):
    model = BillDocument
    extra = 0


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'hospital', 'patient_name', 'gross_total', 'status', 'created_at')
    list_filter = ('status', 'hospital', 'created_at')
    search_fields = ('bill_number', 'patient_name', 'tgnpdcl_id')
    inlines = [LineItemInline, BillDocumentInline]
    raw_id_fields = ('hospital', 'created_by')
    date_hierarchy = 'created_at'
