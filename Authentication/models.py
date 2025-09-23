from django.contrib.auth.models import User
from django.db import models
from emissions.models import Company

ROLE_CHOICES = [
    ('ADMIN', 'Admin'),
    ('OFFICER', 'Environmental Officer'),
    ('TECH', 'Technician'),
    ('GOV', 'Government Official'),
    ('AUDITOR', 'Auditor'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, null=True, blank=True)

def __str__(self):
    return f"{self.user.username} - {self.role}"

