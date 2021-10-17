from django.contrib import admin
from .models import *


class DoctorAdmin(admin.TabularInline):
    model = Doctor


class NurseAdmin(admin.TabularInline):
    model = Nurse


class StaffAdmin(admin.TabularInline):
    model = Staff


class HospitalAdmin(admin.ModelAdmin):
    inlines = [DoctorAdmin, NurseAdmin, StaffAdmin]


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient)
