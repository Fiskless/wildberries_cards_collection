# Generated by Django 4.0.4 on 2022-04-23 22:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_product_time_alter_trackparameter_time_interval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.now, help_text='Время отслеживания товара', verbose_name='Время отслеживания'),
        ),
    ]
