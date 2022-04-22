import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.timezone import utc

TIME_INTERVAL_CHOICES = [
    ('1 hour', '1 час'),
    ('12 hours', '12 часов'),
    ('24 hours', '24 часа'),
]


class TrackParameter(models.Model):

    article = models.CharField(
        verbose_name='артикул',
        max_length=10,
        help_text='Артикул товара',
    )
    start_at = models.DateTimeField(
        verbose_name='начало отслеживания',
        db_index=True,
        help_text='Дата начала периода отслеживания товара',
    )
    end_at = models.DateTimeField(
        verbose_name='Конец отслеживания',
        db_index=True,
        help_text='Дата конца периода отслеживания товара',
    )
    time_interval = models.CharField(
        'Интервал отслеживания',
        max_length=10,
        choices=TIME_INTERVAL_CHOICES,
        default='1 hour')
    user = models.ManyToManyField(
        User,
        related_name='parameters',
        verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Параметр отслеживания'
        verbose_name_plural = 'Параметры отслеживания'

    def __str__(self):
        return f'{self.article}:{self.start_at}:{self.end_at}'


class Product(models.Model):
    """Contains information about the product"""
    article = models.CharField(
        verbose_name='артикул',
        max_length=10,
        help_text='Артикул товара',
    )
    name = models.CharField(
        verbose_name='наименование товара',
        max_length=100,
    )
    price_without_discount = models.IntegerField(
        verbose_name='Цена без скидки',
        validators=[MinValueValidator(0)],
        help_text='Цена без скидки в копейках',
    )
    price_with_discount = models.IntegerField(
        verbose_name='Цена со скидкой',
        validators=[MinValueValidator(0)],
        help_text='Цена со скидкой в копейках',
    )
    brand = models.CharField(
        verbose_name='бренд товара',
        max_length=50,
    )
    seller = models.CharField(
        verbose_name='поставщик',
        max_length=100,
    )
    track = models.ManyToManyField(
        TrackParameter,
        related_name='products',
        verbose_name='Параметры отслеживания')
    time = models.DateTimeField(
        verbose_name='Время отслеживания',
        db_index=True,
        help_text='Время отслеживания товара',
        default=datetime.datetime.now
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.brand}/ {self.name}/ {self.time.strftime("%Y-%m-%d %H:%M")}'
