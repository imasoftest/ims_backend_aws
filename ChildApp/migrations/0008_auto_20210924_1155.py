# Generated by Django 3.0 on 2021-09-24 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ChildApp', '0007_auto_20210922_1134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='child',
            old_name='photo',
            new_name='picture',
        ),
    ]
