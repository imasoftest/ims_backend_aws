# Generated by Django 3.0 on 2021-09-27 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_AddFieldsToLibrary'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchangelibrary',
            name='sattus',
            field=models.BooleanField(null=True),
        ),
    ]
