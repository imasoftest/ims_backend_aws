# Generated by Django 3.0 on 2021-11-26 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChildApp', '0018_auto_20211126_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacyrights',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]