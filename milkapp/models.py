import django.contrib.auth.models
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='')  # Только поддиректория внутри 'media'
    is_active = models.BooleanField(default=True)


class Order(models.Model):
    order_statuses = [
        ("DRAFT", "Черновик"),
        ("DELETED", "Удалён"),
        ("FORMED", "Сформирован"),
        ("COMPLETED", "Завершён"),
        ("REJECTED", "Отклонён"),
    ]
    parent_name = models.CharField(max_length=100)
    services = models.ManyToManyField(Service, related_name='orders')
    status = models.CharField(max_length=100, choices=order_statuses)


class Creator(models.Model):
    creator_types = [
        ("CREATOR", "Создатель"),
        ("MODERATOR", "Модератор"),
    ]
    name = models.CharField(max_length=150, default='')
    type = models.CharField(max_length=150, choices=creator_types, default=creator_types[0])


