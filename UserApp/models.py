import json

from django.contrib.auth.models import AbstractUser
from django.db import models

from anam_backend_main.constants import Parent, Teacher, Admin, SuperAdmin


# Create your models here.

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)


class User(AbstractUser):
    USER_ROLE = [
        (SuperAdmin, 'SuperAdmin'),
        (Parent, 'Parent'),
        (Teacher, 'Teacher'),
        (Admin, 'Admin')
    ]
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=250, null=True)
    phoneNumber = models.CharField(max_length=50, null=True)
    altPhoneNumber = models.CharField(max_length=50, null=True)
    altEmail = models.EmailField(null=True)
    role = models.ForeignKey(Roles, null=True, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="upload/photo", null=True, blank=True)
    classnames = models.CharField(null=True, blank=True, max_length=255)
    notes = models.TextField(null=True)
    dob = models.DateTimeField(null=True)

    def get_classNames(self):
        try:
            data = json.loads(self.classnames)
            if (type(data) == type([])):
                return data
            return []
        except Exception:
            return []


class ClassData(models.Model):
    name = models.CharField(max_length=50)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)


class NationalityData(models.Model):
    name = models.CharField(max_length=50)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
