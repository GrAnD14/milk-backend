from django.db import connection
from django.shortcuts import render, redirect

from .models import *


def get_draft_order():
    return Order.objects.filter(status=1).first()


def index(request):
    query = request.GET.get("query", "")
    products = Product.objects.filter(name__icontains=query).filter(status=1)
    draft_order = get_draft_order()

    context = {
        "query": query,
        "products": products,
        "draft_order_id": draft_order.pk if draft_order else None,
        "order_products_count": draft_order.products.count() if draft_order else None
    }

    return render(request, "home_page.html", context)


def product_details(request, product_id):
    context = {
        "product": Product.objects.get(id=product_id)
    }

    return render(request, "product_page.html", context)


def product_delete(request, product_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE products SET status = 2 WHERE id = %s", [product_id])

    return redirect("/")


def order_details(request, order_id):
    order = Order.objects.get(id=order_id)

    context = {
        "order": order,
        "products": order.products.all()
    }

    return render(request, "order_page.html", context)


def product_add_to_order(request, product_id):
    product = Product.objects.get(pk=product_id)

    order = get_draft_order()

    if order is None:
        order = Order.objects.create()

    order.products.add(product)
    order.save()

    return redirect("/")


def order_delete(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = 5
    order.save()
    return redirect("/")

