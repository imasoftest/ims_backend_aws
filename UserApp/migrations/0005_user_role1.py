# Generated by Django 3.0 on 2021-08-30 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0004_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UserApp.Roles'),
        ),
    ]