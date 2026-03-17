from django.urls import path
from .views import home, shop, category_detail, product_detail

urlpatterns = [
    path("", home, name="home"),
    path("shop/", shop, name="shop"),
    path("category/<slug:slug>/", category_detail, name="category_detail"),
    path("product/<slug:slug>/", product_detail, name="product_detail"),
]
