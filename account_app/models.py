from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField

# App User Model
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True)
    
    ROLES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    )
    roles = models.ManyToManyField('Role', related_name='users')
    
    
    def __str__(self):
        return self.username
    
    
    
# Role Model
class Role(models.Model):
    name = models.CharField(max_length=10, unique=True, choices=User.ROLES)

    def __str__(self):
        return self.name