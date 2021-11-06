from django.contrib import admin
from .models import Patient, Hospital, HospitalStaff


class HospitalStaffAdmin(admin.TabularInline):
    model = HospitalStaff


class HospitalAdmin(admin.ModelAdmin):
    inlines = [HospitalStaffAdmin]


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient)
