from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import PlacementOfficer


class PlacementOfficerSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = PlacementOfficer
        fields = [
            'id',
            'full_name',
            'official_email',
            'country_code',
            'phone_number',
            'organization_name',
            'department',
            'employee_id',
            'designation',
            'password',
            'confirmPassword',
            'registered_on'
        ]
        read_only_fields = ['id', 'registered_on']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError(
                {"confirmPassword": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        validated_data['password'] = make_password(validated_data['password'])
        return PlacementOfficer.objects.create(**validated_data)