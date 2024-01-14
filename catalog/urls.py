from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import CategoryViewSet, LineViewSet, ProductKindViewSet


router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"kinds", ProductKindViewSet)
router.register(r"lines", LineViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
