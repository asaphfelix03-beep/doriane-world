from django.urls import path
from .views import checkout, confirmation

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("checkout/confirmation/<int:order_id>/", confirmation, name="order_confirmation"),
]
