# Generated by Django 3.0 on 2021-09-30 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChildApp', '0008_auto_20210924_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='siblings',
            field=models.CharField(max_length=500, null=True),
        ),
    ]