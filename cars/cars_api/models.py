from django.contrib.auth.models import User
from django.db import models



# Create your models here.

class CarBrand(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.ForeignKey('CarBrand', null=True, on_delete=models.PROTECT, verbose_name="Бренд",
                              related_name='Cars')
    model = models.CharField(max_length=255, verbose_name="Модель")
    description = models.CharField(verbose_name="Описание")
    mileage = models.IntegerField(default=0, verbose_name="Пробег")
    user = models. ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} - {self.model}"
