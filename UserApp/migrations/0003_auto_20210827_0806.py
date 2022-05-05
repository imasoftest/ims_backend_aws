# Generated by Django 3.0 on 2021-08-27 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_imsuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='altEmail',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='altPhoneNumber',
            field=models.IntegerField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phoneNumber',
            field=models.IntegerField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('SuperAdmin', 'SuperAdmin'), ('Parent', 'Parent'), ('Teacher', 'Teacher'), ('Admin', 'Admin')], default='SuperAdmin', max_length=10),
        ),
    ]
