from django.contrib import admin
from user_details.models import Patient, Hospital, HospitalStaff, BlockchainAccess, BlockchainAccessOtp


class HospitalStaffAdmin(admin.TabularInline):
    model = HospitalStaff


class HospitalAdmin(admin.ModelAdmin):
    inlines = [HospitalStaffAdmin]


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient)
admin.site.register(BlockchainAccess)
admin.site.register(BlockchainAccessOtp)
