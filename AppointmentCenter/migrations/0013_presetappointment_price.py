# Generated by Django 3.0 on 2021-11-15 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppointmentCenter', '0012_auto_20211020_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='presetappointment',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]