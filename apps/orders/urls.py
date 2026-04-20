from django.urls import path
from .views import confirmation

urlpatterns = [
    path("checkout/confirmation/<int:order_id>/", confirmation, name="order_confirmation"),
]
