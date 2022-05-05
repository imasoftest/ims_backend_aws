# Generated by Django 3.0 on 2021-10-11 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0016_changepathofuserimage'),
        ('AppointmentCenter', '0005_auto_20210922_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='presetappointment',
            name='endDateTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='presetappointment',
            name='startDateTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='presetappointment',
            name='className',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.ClassData'),
        ),
        migrations.AlterField(
            model_name='presetappointment',
            name='presetInfo',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='presetappointment',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='presetappointment',
            name='child',
        ),
        migrations.RemoveField(
            model_name='presetappointment',
            name='timerange',
        ),
    ]
