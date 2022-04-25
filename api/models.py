from django.db import models
from anam_backend_main.constants import Classroom, All
# Create your models here.
import jsonfield 

class SchoolDocument(models.Model):
    ForSelect = [
        (Classroom, 'Classroom'),
        (All, 'All'),
    ]
    name = models.CharField(max_length=255)
    url = models.FileField(upload_to='schooldocument')
    # documentfor = models.CharField(max_length=255, choices=ForSelect,default=All)
    documentfor = models.CharField(max_length=255, default=All)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MiniClub(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(max_length=255, null = True)
    startDate = models.DateTimeField(max_length=255,null=True)
    endDate = models.DateTimeField(max_length=255,null=True)
    price = models.FloatField()
    limit = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    children = models.ManyToManyField('ChildApp.Child', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isPaid = jsonfield.JSONField(null=True)


class BookStatus(models.TextChoices):
    PRESENT = 'present'
    RENTED = 'rented'


class ExchangeLibrary(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='exchangelibrary',null=True)
    child = models.ForeignKey('ChildApp.Child', blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=BookStatus.choices, default=BookStatus.PRESENT)
    donator = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    booked_status = models.BooleanField(default=False)
    booked_on = models.DateTimeField(null = True,blank=True)
    returned_on = models.DateTimeField(null = True, blank=True)
    


class Marketing(models.Model):
    question = models.CharField(max_length=255)
    content = models.TextField()
    poster = models.ForeignKey('UserApp.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)