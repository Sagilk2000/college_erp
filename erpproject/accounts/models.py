from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('utype', 'admin')
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    User_Type = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student')

    )
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    utype = models.CharField(max_length=10, choices=User_Type, default='student')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['utype', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.utype})"

