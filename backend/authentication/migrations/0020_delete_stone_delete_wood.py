# Generated by Django 4.1.7 on 2023-05-01 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_followuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stone',
        ),
        migrations.DeleteModel(
            name='Wood',
        ),
    ]
