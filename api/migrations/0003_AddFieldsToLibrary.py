# Generated by Django 3.0 on 2021-09-27 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_exchangelibrary_donator'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchangelibrary',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='exchangelibrary',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
