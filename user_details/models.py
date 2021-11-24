from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

ALPHA_REGEX = RegexValidator('^[a-zA-Z ]*$', 'Only alphabets are allowed')
ZIP_CODE_REGEX = RegexValidator('^[1-9][0-9]*$', 'Only numeric characters of length 6 is allowed')


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient')
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
    state = models.CharField(max_length=127)
    mobile = PhoneNumberField()

    def __str__(self):
        return self.user.username


class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='hospital')
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    contact = PhoneNumberField()
    landline = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6, validators=[ZIP_CODE_REGEX])
    city = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    state = models.CharField(max_length=127)
    web = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class HospitalStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='hospital_staff')
    hos_code = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('D', 'Doctor'),
        ('N', 'Nurse'),
        ('S', 'Staff'),
        ('O', 'Other'),
    ]
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    degree = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    department = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    designation = models.CharField(max_length=127, validators=[ALPHA_REGEX])
    contact = PhoneNumberField()

    def __str__(self):
        return self.user.username


class BlockchainAccess(models.Model):
    primary = models.ForeignKey(Patient, related_name="primary_actors", on_delete=models.CASCADE)
    secondary = models.ForeignKey(Hospital, related_name="secondary_actors", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("primary", "secondary")
