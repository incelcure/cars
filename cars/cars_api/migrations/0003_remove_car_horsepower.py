# Generated by Django 5.0.1 on 2024-01-31 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_api', '0002_rename_cars_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='horsepower',
        ),
    ]
