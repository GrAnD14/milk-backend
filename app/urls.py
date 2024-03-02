from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('product/<int:product_id>', product),
    path('orders/<int:order_id>', order),
]