from rest_framework import serializers
from .models import Patient, Hospital


class PatientSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    class Meta:
        model = Patient
        fields = ('user', 'dob', 'gender', 'nationality', 'marital_status',
                  'occupation', 'emergency_contact_name', 'emergency_contact_phone',
                  'emergency_contact_email', 'emergency_contact_relation',
                  'address', 'zip_code', 'city', 'state', 'mobile')


class HospitalSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    class Meta:
        model = Hospital
        fields = ('user', 'type', 'description',
                  'contact', 'landline', 'address',
                  'zip_code', 'city', 'state', 'web')
