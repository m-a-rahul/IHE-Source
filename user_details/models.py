from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

ALPHA_REGEX = RegexValidator('^[a-zA-Z ]*$', 'Only alphabets are allowed')
ZIP_CODE_REGEX = RegexValidator('^[1-9][0-9]*$', 'Only numeric characters of length 6 is allowed')


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nationality = CountryField()
    MARITAL_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('D', 'Divorced'),
    ]
    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES)
    occupation = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    emergency_contact_name = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    emergency_contact_phone = PhoneNumberField()
    emergency_contact_email = models.EmailField()
    emergency_contact_relation = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6, validators=[ZIP_CODE_REGEX])
    city = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    state = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    mobile = PhoneNumberField()

    def __str__(self):
        return self.user.username


class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    contact = PhoneNumberField()
    landline = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6, validators=[ZIP_CODE_REGEX])
    city = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    state = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    web = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hos_code = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=200)
    imai = models.CharField(max_length=200)
    aadharno = models.CharField(max_length=12)
    degree = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    contact = models.CharField(max_length=13)

    def __str__(self):
        return self.user.username


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hos_code = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    aadharno = models.CharField(max_length=12)
    contact = models.CharField(max_length=13)

    def __str__(self):
        return self.user.username


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hos_code = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=200)
    imai = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    aadharno = models.CharField(max_length=12)
    contact = models.CharField(max_length=13)

    def __str__(self):
        return self.user.username
