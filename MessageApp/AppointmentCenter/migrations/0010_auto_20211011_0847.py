# Generated by Django 3.0 on 2021-10-11 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ChildApp', '0012_auto_20211007_1027'),
        ('AppointmentCenter', '0009_presetappointmentsessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presetappointmentsessions',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ChildApp.Child'),
        ),
    ]