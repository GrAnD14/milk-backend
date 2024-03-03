# Generated by Django 4.2.5 on 2024-02-05 13:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_order_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 13, 13, 16, 849033, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]
