from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import PlacementOfficer

#registration
#placement officer

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

#recruiter registration

from .models import Recruiter

class RecruiterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recruiter
        fields = '__all__'   

#student registration

from django.contrib.auth import get_user_model
from django.db import transaction
from .models import StudentProfile
import re

User = get_user_model()

class StudentRegistrationSerializer(serializers.Serializer):
    fullName = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    countryCode = serializers.CharField(max_length=10, default='+1')
    phoneNumber = serializers.CharField(max_length=20)
    InstitutionName = serializers.CharField(max_length=255)
    Degree = serializers.CharField(max_length=100)
    GraduationYear = serializers.IntegerField()
    StudentID = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_StudentID(self, value):
        if StudentProfile.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("A student with this ID is already registered.")
        return value

    def validate(self, data):
        # 1. Password Matching Check
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError({"confirmPassword": "Passwords do not match."})

        # 2. Strong Password Validation
        password = data['password']
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter."})
        if not re.search(r"\d", password):
            raise serializers.ValidationError({"password": "Password must contain at least one number."})
        if not re.search(r"[!@#$%^&*]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one special character."})

        # 3. Phone Number Format (10 digits)
        phone = data['phoneNumber']
        if not re.match(r"^\d{10}$", phone):
            raise serializers.ValidationError({"phoneNumber": "Phone number must be exactly 10 digits."})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirmPassword')

        fullName = validated_data.pop('fullName')
        email = validated_data.pop('email')

        with transaction.atomic():
            user = User.objects.create_user(
                email=email,
                username=email,
                full_name=fullName,
                password=password,
                role=User.Role.STUDENT
            )

            StudentProfile.objects.create(
                user=user,
                country_code=validated_data.pop('countryCode'),
                phone_number=validated_data.pop('phoneNumber'),
                institution_name=validated_data.pop('InstitutionName'),
                degree=validated_data.pop('Degree'),
                graduation_year=validated_data.pop('GraduationYear'),
                student_id=validated_data.pop('StudentID')
            )

        return user
    
#training coordinator

from .models import StudentCoordinator

class StudentCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCoordinator
        fields = '__all__'
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }