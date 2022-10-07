from django.urls import path, include
from rest_framework import routers

from api.viewsets import SaleViewSet, ClientViewSet, ProductViewSet, SellerViewSet, OrdersSaleViewSet
from django.conf.urls.static import static

from pdv import settings

router = routers.DefaultRouter()
router.register('clients', ClientViewSet, basename="clients")
router.register('sellers', SellerViewSet)
router.register('products', ProductViewSet)
router.register('sales', SaleViewSet)
router.register('orders', OrdersSaleViewSet)

urlpatterns = [
    path("", include(router.urls)),

]+static(settings.STATIC_URL)
