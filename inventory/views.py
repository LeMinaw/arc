from django.db.models import Count, Max, Q
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from catalog.models import Product
from inventory.models import Item, TestBench
from inventory.serializers import (
    ItemSerializer,
    ProductStockSerializer,
    TestBenchSerializer,
)


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.order_by("-mod_date")

    serializer_class = ItemSerializer


class StockViewSet(ModelViewSet):
    queryset = (
        Product.objects.annotate(
            in_stock_count=Count("stock", filter=Q(stock__in_stock=True)),
            last_mod_date=Max("stock__mod_date", filter=Q(stock__in_stock=True)),
        )
        .filter(in_stock_count__gt=0)
        .order_by("-last_mod_date")
    )

    serializer_class = ProductStockSerializer

    filterset_fields = ["kind"]


class TestBenchViewSet(ReadOnlyModelViewSet):
    queryset = TestBench.objects.all()

    serializer_class = TestBenchSerializer
