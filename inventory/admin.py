from django.contrib.admin import register

from common.admin import BaseAdmin, BaseStackedInline
from common.utils import short_description
from inventory.models import Item, Test, TestBench


class TestInline(BaseStackedInline):
    model = Test

    # extra = 0


@register(Test)
class TestAdmin(BaseAdmin):
    date_hierarchy = "date"

    readonly_fields = ["date"]


@register(TestBench)
class TestBenchAdmin(BaseAdmin):
    autocomplete_fields = ["kind"]


@register(Item)
class ItemAdmin(BaseAdmin):
    list_display = ["__str__", "in_stock", "id", "reference", "add_date", "out_date"]

    list_filter = ["product__kind", "product__line", "in_stock"]

    date_hierarchy = "mod_date"

    inlines = [TestInline]

    readonly_fields = ["id", "mod_date", "add_date"]

    autocomplete_fields = ["product"]

    @short_description("référence")
    def reference(self, obj):
        return obj.product.reference
