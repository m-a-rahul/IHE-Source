from rest_framework import serializers
from .models import Patient, Hospital


class PatientSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    class Meta:
        model = Patient
        fields = ('user', 'dob', 'gender', 'nationality', 'maritial_status',
                  'occupation', 'arname', 'arno', 'aremail', 'arrelation',
                  'address', 'pin_code', 'city', 'state', 'mobile', 'aadhar')


class HospitalSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    class Meta:
        model = Hospital
        fields = ('user', 'doi', 'imai', 'bed_count', 'type',
                  'contact', 'landline1', 'landline2', 'gstin', 'email2',
                  'address', 'pin_code', 'city', 'state', 'web')
