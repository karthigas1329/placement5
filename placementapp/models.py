from django.db import models

#registration 

#placementofficer

class PlacementOfficer(models.Model):
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('trainer', 'Trainer'),
        ('admin', 'Administrator'),
    ]

    full_name = models.CharField(max_length=200)
    official_email = models.EmailField(unique=True)
    country_code = models.CharField(max_length=10, default="+91")
    phone_number = models.CharField(max_length=15)
    organization_name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    password = models.CharField(max_length=255)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
 #recruiter registration

class Recruiter(models.Model):
    hr_id = models.CharField(max_length=20, unique=True)
    registered_on = models.CharField(max_length=20)

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)

    company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    password = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name
       
#student registration

from django.contrib.auth.models import AbstractUser

class StudentRegistration(models.Model):
    # Use email as primary authentication field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        RECRUITER = 'RECRUITER', 'Recruiter'
        TRAINING_COORDINATOR = 'TRAINING_COORDINATOR', 'Training Coordinator'
        PLACEMENT_OFFICER = 'PLACEMENT_OFFICER', 'Placement Officer'
        
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    
    # We allow blank/null usernames as authentication defaults to email
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.email} ({self.role})"


class StudentProfile(models.Model):
    StudentProfile = models.OneToOneField(StudentRegistration, on_delete=models.CASCADE, related_name='student_profile')
    country_code = models.CharField(max_length=10, default='+1')
    phone_number = models.CharField(max_length=20)
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    student_id = models.CharField(max_length=50, unique=True)
    registered_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Student Profile for {self.StudentProfile.email}"

#training coordinaator

class StudentCoordinator(models.Model):

    DESIGNATION_CHOICES = [
    ("","Select Specific Role"),
    ("professor", "Professor"),
    ("trainer", "Trainer"),
    ("admin", "Administrator"),
    ]

    full_name = models.CharField(max_length=100)
    official_email = models.EmailField(unique=True)
    country_code = models.CharField(max_length=5, default="+91")
    phone_number = models.CharField(max_length=10, unique=True)
    organization_name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=30, unique=True)
    designation = models.CharField(max_length=20,choices=DESIGNATION_CHOICES,)
    password = models.CharField(max_length=255)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

#login
#common login 

from .managers import UserManager

class commonlogin(AbstractUser):

    ROLE_CHOICES = (
        ("student", "Student"),
        ("recruiter", "Recruiter"),
        ("placement_officer", "Placement Officer"),
        ("training_coordinator", "Training Coordinator"),
    )
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=30,choices=ROLE_CHOICES)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    
#placementofficerlogin


class PlacementOfficerlogin(models.Model):

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
#recruiterlogin

class RecruiterLogin(models.Model):

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#studentlogin
class Studentlogin(models.Model):
    # Use email as primary authentication field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        RECRUITER = 'RECRUITER', 'Recruiter'
        TRAINING_COORDINATOR = 'TRAINING_COORDINATOR', 'Training Coordinator'
        PLACEMENT_OFFICER = 'PLACEMENT_OFFICER', 'Placement Officer'
        
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    
    # We allow blank/null usernames as authentication defaults to email
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.email} ({self.role})"

#trainingcoordinator login

from django.contrib.auth.hashers import make_password

class TrainingCoordinator(models.Model):
    full_name = models.CharField(max_length=150)
    official_email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    
#adminlogin

from django.contrib.auth.hashers import make_password, check_password
class Admin(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email