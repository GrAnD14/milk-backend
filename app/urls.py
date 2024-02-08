from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/products/search/', search_products),  # GET
    path('api/products/<int:product_id>/', get_product_by_id),  # GET
    path('api/products/<int:product_id>/image/', get_product_image),  # GET
    path('api/products/<int:product_id>/update/', update_product),  # PUT
    path('api/products/<int:product_id>/update_image/', update_product_image),  # PUT
    path('api/products/<int:product_id>/delete/', delete_product),  # DELETE
    path('api/products/create/', create_product),  # POST
    path('api/products/<int:product_id>/add_to_order/', add_product_to_order),  # POST

    # Набор методов для заявок
    path('api/orders/search/', search_orders),  # GET
    path('api/orders/<int:order_id>/', get_order_by_id),  # GET
    path('api/orders/<int:order_id>/update/', update_order),  # PUT
    path('api/orders/<int:order_id>/update_status_user/', update_status_user),  # PUT
    path('api/orders/<int:order_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/orders/<int:order_id>/delete/', delete_order),  # DELETE
    path('api/orders/<int:order_id>/delete_product/<int:product_id>/', delete_product_from_order),  # DELETE
]
