from django_filters import BooleanFilter, FilterSet
from rest_framework.viewsets import ModelViewSet

from catalog.models import Category, Line, ProductKind
from catalog.serializers import (
    LineSerializer,
    ProductKindSerializer,
)


class CategoryFilter(FilterSet):
    root = BooleanFilter(field_name="parent", lookup_expr="isnull")

    class Meta:
        model = Category
        fields = ["parent", "slug"]


class LineViewSet(ModelViewSet):
    queryset = Line.objects.all()

    serializer_class = LineSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    filterset_class = CategoryFilter

    serializer_class = ProductKindSerializer


class ProductKindViewSet(ModelViewSet):
    queryset = ProductKind.objects.all()

    serializer_class = ProductKindSerializer
