from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=20)
    maritial_status = models.CharField(max_length=15)
    occupation = models.CharField(max_length=200)
    arname = models.CharField(max_length=200)
    arno = models.CharField(max_length=200)
    aremail = models.EmailField
    arrelation = models.CharField(max_length=200)
    address = models.TextField
    pin_code = models.IntegerField
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    mobile = models.CharField(max_length=13)
    email = models.EmailField
    aadhar = models.CharField(max_length=12)


class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    doi = models.DateField
    imai = models.CharField(max_length=200)
    bed_count = models.IntegerField
    type = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    landline1 = models.CharField(max_length=200)
    landline2 = models.CharField(max_length=200, blank=True, null=True)
    gstin = models.CharField(max_length=200)
    address = models.TextField
    pin_code = models.IntegerField
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    mobile = models.CharField(max_length=13)
    email1 = models.EmailField
    email2 = models.EmailField(blank=True, null=True)
    doctor_count = models.IntegerField
    web = models.URLField(blank=True, null=True)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hos_code = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dob = models.DateField
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=200)
    imai = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    contact = models.CharField(max_length=13)
    email = models.EmailField


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hos_code = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dob = models.DateField
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    aadharno = models.CharField(max_length=12)
    contact = models.CharField(max_length=13)
    email = models.EmailField


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hos_code = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dob = models.DateField
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=200)
    imai = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    aadharno = models.CharField(max_length=12)
    contact = models.CharField(max_length=13)
    email = models.EmailField
