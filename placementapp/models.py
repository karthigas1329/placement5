from django.db import models

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
