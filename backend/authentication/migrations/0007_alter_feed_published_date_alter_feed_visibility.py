# Generated by Django 4.1.7 on 2023-04-25 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_pp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Veröffentlicht'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='visibility',
            field=models.BooleanField(default=True, verbose_name='Sichtbar'),
        ),
    ]
