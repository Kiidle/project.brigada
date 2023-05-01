# Generated by Django 4.1.7 on 2023-05-01 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_alter_user_majestic_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='majestic_id',
            field=models.PositiveIntegerField(null=True, unique=True, verbose_name='Majestic ID'),
        ),
    ]