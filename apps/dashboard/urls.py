from django.urls import path
from .views import order_list

urlpatterns = [
    path("dashboard/", order_list, name="dashboard_orders"),
]
