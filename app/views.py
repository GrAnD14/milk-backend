import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime, parse_date
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_order(request):
    user = identity_user(request)

    if user is None:
        return None

    order = Order.objects.filter(owner_id=user.id).filter(status=1).first()

    return order


@api_view(["GET"])
def search_products(request):
    query = request.GET.get("query", "")

    product = Product.objects.filter(status=1).filter(name__icontains=query)

    serializer = ProductSerializer(product, many=True)

    draft_order = get_draft_order(request)

    resp = {
        "products": serializer.data,
        "draft_order_id": draft_order.pk if draft_order else None
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
@permission_classes([IsModerator])
def update_product(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_product(request):
    product = Product.objects.create()

    serializer = ProductSerializer(product)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)
    product.status = 2
    product.save()

    product = Product.objects.filter(status=1)
    serializer = ProductSerializer(product, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product_to_order(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)

    order = get_draft_order(request)

    if order is None:
        order = Order.objects.create()

    if order.products.contains(product):
        return Response(status=status.HTTP_409_CONFLICT)

    order.products.add(product)
    order.owner = identity_user(request)
    order.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_product_image(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)

    return HttpResponse(product.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_product_image(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_orders(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    orders = Order.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        orders = orders.filter(owner=user)

    if status_id != -1:
        orders = orders.filter(status=status_id)

    if date_start and parse_datetime(date_start):
        orders = orders.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        orders = orders.filter(date_formation__lt=parse_datetime(date_end))

    serializer = OrdersSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_order_delivery_date(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    delivery_date = request.data.get("delivery_date")
    if delivery_date and parse_date(delivery_date):
        order.delivery_date = parse_date(delivery_date)
        order.save()

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    order.status = 2
    order.date_formation = timezone.now()
    order.save()

    calculate_delivery_date(order_id)

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


def calculate_delivery_date(order_id):
    data = {
        "order_id": order_id
    }

    requests.post("http://127.0.0.1:8080/calc_delivery_date/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)

    if order.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = request_status
    order.date_complete = timezone.now()
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 5
    order.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product_from_order(request, order_id, product_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Product.objects.filter(pk=product_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    order.products.remove(Product.objects.get(pk=product_id))
    order.save()

    if order.products.count() == 0:
        order.delete()
        return Response(status=status.HTTP_201_CREATED)

    serializer = OrderSerializer(order)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован!',
        'user_id': user.id,
        "access_token": access_token
    }
    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check(request):
    user = identity_user(request)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {
        "message": "Вы успешно вышли из аккаунта"
    }

    return Response(message, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsModerator])
def get_users(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsModerator])
def make_moderator(request, user_id):
    if not CustomUser.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = CustomUser.objects.get(pk=user_id)
    user.is_moderator = True
    user.save()

    return Response(status=status.HTTP_200_OK)