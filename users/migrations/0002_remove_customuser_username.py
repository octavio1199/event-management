# Generated by Django 4.2.13 on 2024-06-21 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
