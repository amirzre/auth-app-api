# Generated by Django 5.0.7 on 2024-08-12 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='phone_verified',
        ),
    ]
