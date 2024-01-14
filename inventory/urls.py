from django.urls import include, path
from rest_framework.routers import DefaultRouter

from inventory.views import ItemViewSet, StockViewSet, TestBenchViewSet


router = DefaultRouter()
router.register(r"items", ItemViewSet)
router.register(r"stock", StockViewSet)
router.register(r"test-bench", TestBenchViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
