# Generated by Django 4.1.7 on 2023-04-26 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_rename_privacy_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ['-published_date', '-id']},
        ),
    ]