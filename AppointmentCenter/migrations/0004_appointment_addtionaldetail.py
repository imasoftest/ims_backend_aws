# Generated by Django 3.0 on 2020-11-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppointmentCenter', '0003_auto_20201009_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='addtionalDetail',
            field=models.TextField(blank=True, null=True),
        ),
    ]