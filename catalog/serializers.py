from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ListField,
    SerializerMethodField,
)

from catalog.models import Category, Line, Manufacturer, Product, ProductKind


class ManufacturerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ["name", "logo_url"]


class LineSerializer(HyperlinkedModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)

    class Meta:
        model = Line
        fields = ["id", "manufacturer", "name"]


class SimpleCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "name", "parent"]


class CategorySerializer(HyperlinkedModelSerializer):
    specs_schema = SerializerMethodField()
    parents = ListField(child=SimpleCategorySerializer())

    def get_specs_schema(self, obj):
        return obj.coalesce_specs_schema()

    class Meta(SimpleCategorySerializer.Meta):
        fields = [*SimpleCategorySerializer.Meta.fields, "specs_schema", "parents"]


class ProductKindSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        model = ProductKind


class ProductSerializer(HyperlinkedModelSerializer):
    line_id = SerializerMethodField()
    line_name = SerializerMethodField()
    logo = SerializerMethodField()

    def get_line_id(self, obj):
        return getattr(obj.line, "id", None)

    def get_line_name(self, obj):
        return str(obj.line) if obj.line else None

    def get_logo(self, obj):
        return obj.line.manufacturer.logo_url if obj.line else None

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "kind",
            "line",
            "line_id",
            "line_name",
            "logo",
            "reference",
            "link",
            "image",
            "specs",
        ]
