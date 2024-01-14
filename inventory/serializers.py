from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ListSerializer,
    SerializerMethodField,
)

from catalog.serializers import ProductSerializer
from inventory.models import Item, Test, TestBench


class ProductStockSerializer(ProductSerializer):
    last_mod_date = SerializerMethodField()

    def get_last_mod_date(self, obj):
        return obj.stock.latest().mod_date

    class Meta(ProductSerializer.Meta):
        fields = [*ProductSerializer.Meta.fields, "stock", "last_mod_date"]


class TestSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ["date", "data"]


class TestBenchSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = TestBench
        fields = ["data_schema"]


class ItemSerializer(HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)
    test = TestSerializer(read_only=True)
    test_bench = TestBenchSerializer(read_only=True)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()

        for field in cls.Meta.list_excluded_fields:
            kwargs["child"].fields.pop(field)

        return ListSerializer(*args, **kwargs)

    class Meta:
        model = Item
        fields = ["product", "in_stock", "add_date", "mod_date", "test", "test_bench"]
        list_excluded_fields = ["test_bench"]
