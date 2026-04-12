from django.urls import path
from .views import (
    cart_detail,
    add_to_cart,
    update_cart,
    remove_from_cart,
    quick_order_whatsapp,
)

urlpatterns = [
    path("cart/", cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/update/", update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/quick/whatsapp/", quick_order_whatsapp, name="quick_order_whatsapp"),
]
