# Generated by Django 4.1.7 on 2023-04-26 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_commentary_options_privacy'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Privacy',
            new_name='Settings',
        ),
    ]