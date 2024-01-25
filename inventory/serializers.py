from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ListSerializer,
    SerializerMethodField,
)

from catalog.serializers import ProductSerializer
from common.exceptions import to_serializer_validation_error
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
    name = SerializerMethodField()
    product = ProductSerializer(read_only=True)
    specs_schema = SerializerMethodField()
    test = TestSerializer()
    test_bench = TestBenchSerializer(read_only=True)

    def get_name(self, obj):
        return str(obj)

    def get_specs_schema(self, obj):
        return obj.product.kind.item_specs_schema

    @to_serializer_validation_error
    def create(self, validated_data):
        """Overriden to allow writes on nested test data."""

        test_data = validated_data.pop("test", None)
        item = super().create(validated_data)

        if test_data:
            Test.objects.create(item=item, **test_data)

        return item

    @to_serializer_validation_error
    def update(self, instance, validated_data):
        """Overriden to allow writes on nested test data."""

        if "test" not in validated_data:
            return super().update(instance, validated_data)

        test_data = validated_data.pop("test")
        item = super().update(instance, validated_data)

        self._update_test(item, test_data)

        return item

    def _update_test(self, instance, test_data):
        if not test_data:
            instance.test = None
            instance.save()
            return

        try:
            test = instance.test
            test.data = test_data.get("data", test.data)
            test.save()
        except ObjectDoesNotExist:
            Test.objects.create(item=instance, **test_data)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()

        for field in cls.Meta.list_excluded_fields:
            kwargs["child"].fields.pop(field)

        return ListSerializer(*args, **kwargs)

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "product",
            "in_stock",
            "add_date",
            "mod_date",
            "out_date",
            "specs",
            "specs_schema",
            "test",
            "test_bench",
        ]
        list_excluded_fields = ["specs_schema", "test_bench"]
