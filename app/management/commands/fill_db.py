import random

from django.core import management
from django.core.management.base import BaseCommand
from ...models import *
from .utils import random_date, random_timedelta


def add_products():
    Product.objects.create(
        name="Молоко",
        description="Один из самых полезных для человека продуктов. Оно богато белком, витаминами A и D, кальцием. Недаром с давних пор люди стали не только покупать молоко оптом, но и придумывать рецепты изготовления из него разных продуктов.",
        price=100,
        image="products/1.png"
    )

    Product.objects.create(
        name="Творог",
        description="Он производится из пастеризованного молока, в которое добавляют закваску, после чего через некоторое время из образовавшейся зернистой массы удаляют сыворотку. Творог необычайно богат белком, витаминами группы В и незаменим в диетическом питании.",
        price=80,
        image="products/2.png"
    )

    Product.objects.create(
        name="Сливки",
        description="Изготавливаются с древнейших времен и представляют собой верхний, самый жирный слой отстоявшегося молока. Они очень калорийны и питательны, насыщены витаминами А, D и Е.",
        price=200,
        image="products/3.png"
    )

    Product.objects.create(
        name="Сметана",
        description="Получается из сливок путем добавления специальной закваски. Особенно популярна она в кухне славянских народов. Сметана богата белком и жирами, содержит витамины А, Е, В12.",
        price=50,
        image="products/4.png"
    )

    Product.objects.create(
        name="Кефир",
        description="Производится с помощью особого кефирного грибка. Очень полезен для здоровья, так же как и другие кисломолочные напитки (простокваша, ряженка, варенец, ацидофилин, мацони и т. д.).",
        price=120,
        image="products/5.png"
    )

    Product.objects.create(
        name="Сыр",
        description="Секрет его изготовления – закваска, содержащая молочнокислые бактерии или особые ферменты. Он очень полезен, богат белком, жиром, витаминами всех групп и кальцием.",
        price=350,
        image="products/6.png"
    )
    
    print("Услуги добавлены")


def add_orders():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    products = Product.objects.all()

    for _ in range(30):
        order = Order.objects.create()
        order.status = random.randint(2, 5)
        order.owner = random.choice(owners)

        if order.status in [3, 4]:
            order.date_complete = random_date()
            order.date_formation = order.date_complete - random_timedelta()
            order.date_created = order.date_formation - random_timedelta()
            order.moderator = random.choice(moderators)
        else:
            order.date_formation = random_date()
            order.date_created = order.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            order.products.add(random.choice(products))

        order.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_products()
        add_orders()









