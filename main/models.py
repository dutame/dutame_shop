from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural ='категории'
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural ='товары'
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    size = models.TextField(null=True, default='BIG', verbose_name='объём, размер')
    date_end = models.DateField(verbose_name='Срок годности')

    def __str__(self):
        return self.title


class ConfirmCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.code

