# Generated by Django 5.0.1 on 2024-01-31 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_api', '0005_car_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='brand',
        ),
        migrations.DeleteModel(
            name='CarBrand',
        ),
    ]