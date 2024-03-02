from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('products/<int:product_id>/', product_details),
    path('products/<int:product_id>/delete/', product_delete),
    path('products/<int:product_id>/add_to_order/', product_add_to_order),
    path('orders/<int:order_id>/', order_details),
    path('orders/<int:order_id>/delete/', order_delete),
]
