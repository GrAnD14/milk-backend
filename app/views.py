from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


def get_draft_order():
    return Order.objects.filter(status=1).first()


@api_view(["GET"])
def search_products(request):
    query = request.GET.get("query", "")

    products = Product.objects.filter(status=1).filter(name__icontains=query)

    serializer = ProductSerializer(products, many=True)

    draft_order = get_draft_order()

    resp = {
        "products": serializer.data,
        "draft_order": draft_order.pk if draft_order else None
    }

    return Response(resp)


@api_view(["GET"])
def get_product_by_id(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_product(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_product(request):
    Product.objects.create()

    products = Product.objects.filter(status=1)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_product(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)
    product.status = 2
    product.save()

    products = Product.objects.filter(status=1)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_product_to_order(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)

    order = Order.objects.filter(status=1).last()

    if order is None:
        order = Order.objects.create()

    order.products.add(product)
    order.save()

    serializer = ProductSerializer(order.products, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_product_image(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)

    return HttpResponse(product.image, content_type="image/png")


@api_view(["PUT"])
def update_product_image(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return HttpResponse(product.image, content_type="image/png")


@api_view(["GET"])
def search_orders(request):
    status = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    orders = Order.objects.exclude(status__in=[1, 5])

    if status != -1:
        orders = orders.filter(status=status)

    if date_start and parse_datetime(date_start):
        orders = orders.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        orders = orders.filter(date_formation__lte=parse_datetime(date_end))

    serializer = OrdersSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_order_by_id(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 2
    order.date_formation = timezone.now()
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)

    if order.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.date_complete = timezone.now()
    order.status = request_status
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 5
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_product_from_order(request, order_id, product_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    order.products.remove(Product.objects.get(pk=product_id))
    order.save()
    
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data["products"])