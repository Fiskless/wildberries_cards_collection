# Generated by Django 4.0.4 on 2022-04-17 10:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(help_text='Артикул товара', max_length=10, verbose_name='артикул')),
                ('name', models.CharField(max_length=100, verbose_name='наименование товара')),
                ('price_without_discount', models.IntegerField(help_text='Цена без скидки в копейках', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена без скидки')),
                ('price_with_discount', models.IntegerField(help_text='Цена со скидкой в копейках', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена со скидкой')),
                ('brand', models.CharField(max_length=50, verbose_name='бренд товара')),
                ('seller', models.CharField(max_length=100, verbose_name='поставщик')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='TrackParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(help_text='Артикул товара', max_length=10, verbose_name='артикул')),
                ('start_at', models.DateTimeField(db_index=True, help_text='Дата начала периода отслеживания товара', verbose_name='начало отслеживания')),
                ('end_at', models.DateTimeField(db_index=True, help_text='Дата конца периода отслеживания товара', verbose_name='Конец отслеживания')),
                ('time_interval', models.CharField(choices=[('1 hour', '1 час'), ('12 hours', '12 часов'), ('24 hours', '24 часа')], default='1hour', max_length=10, verbose_name='Длительность отслеживания')),
                ('user', models.ManyToManyField(related_name='parameters', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Параметр отслеживания',
                'verbose_name_plural': 'Параметры отслеживания',
            },
        ),
    ]
