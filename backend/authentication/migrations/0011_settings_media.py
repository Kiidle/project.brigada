# Generated by Django 4.1.7 on 2023-05-01 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_feed_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='media',
            field=models.BooleanField(default=False, verbose_name='Medien'),
        ),
    ]
