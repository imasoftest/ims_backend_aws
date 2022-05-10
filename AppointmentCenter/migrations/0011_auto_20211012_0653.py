# Generated by Django 3.0 on 2021-10-12 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppointmentCenter', '0010_auto_20211011_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presetappointment',
            name='endDateTime',
        ),
        migrations.RemoveField(
            model_name='presetappointment',
            name='startDateTime',
        ),
        migrations.AddField(
            model_name='presetappointment',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='presetappointment',
            name='endDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='presetappointment',
            name='endTime',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='presetappointment',
            name='startDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='presetappointment',
            name='startTime',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='presetappointment',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]