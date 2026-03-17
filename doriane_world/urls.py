from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.api import CategoryViewSet, ProductViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.products.urls")),
    path("", include("apps.cart.urls")),
    path("", include("apps.orders.urls")),
    path("", include("apps.dashboard.urls")),
    path("api/", include(router.urls)),
]

if settings.DEBUG or settings.SERVE_MEDIA:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
