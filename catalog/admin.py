import json
from copy import deepcopy

from django.contrib.admin import register
from django.forms import Field, HiddenInput, ModelForm
from django.template.loader import render_to_string

from catalog.models import Category, Line, Manufacturer, Product, ProductKind
from common.admin import BaseAdmin
from common.utils import JSONSetEncoder, short_description
from common.widgets import JSONEditorWidget


class CategoryForm(ModelForm):
    coalesced_specs_schema = Field(
        disabled=True,
        required=False,
        widget=HiddenInput(),
        label="Schéma de spécifications global",
        help_text=(
            "Fusion des schémas de toutes les catégories parentes. Lecture seule."
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        coalesced_specs_schema = self.fields["coalesced_specs_schema"]

        if hasattr(self.instance, "parent"):
            coalesced_specs_schema.widget = JSONEditorWidget()
            coalesced_specs_schema.initial = json.dumps(
                self.instance.coalesce_specs_schema(), cls=JSONSetEncoder
            )

    class Meta:
        fields = "__all__"
        model = Category


class ProductForm(ModelForm):
    specs_schema = Field(
        disabled=True,
        required=False,
        widget=HiddenInput(),
        label="Schéma de spécifications",
        help_text="Schéma auquel doivent répondre les spécifications. Lecture seule.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        specs_schema = self.fields["specs_schema"]

        if hasattr(self.instance, "kind"):
            specs_schema.widget = JSONEditorWidget()
            specs_schema.initial = json.dumps(
                self.instance.get_specs_schema(), cls=JSONSetEncoder
            )

    class Meta:
        fields = "__all__"
        model = Product


@register(Manufacturer)
class ManufacturerAdmin(BaseAdmin):
    ordering = ["name"]


@register(Line)
class LineAdmin(BaseAdmin):
    list_filter = ["manufacturer"]

    ordering = ["manufacturer__name", "name"]

    search_fields = ["manufacturer__name", "name"]


@register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ["__str__", "parents", "slug"]

    ordering = ["name"]

    form = CategoryForm

    readonly_fields = ["parents"]

    search_fields = ["name"]

    prepopulated_fields = {"slug": ["name"]}

    fieldsets = [
        (
            None,
            {
                "fields": [("parents", "parent"), ("name", "slug"), "specs_schema"],
            },
        ),
        (
            "Propriétés avancées",
            {
                "classes": ["collapse"],
                "fields": ["coalesced_specs_schema"],
            },
        ),
    ]

    @short_description("hiérarchie")
    def parents(self, obj):
        return render_to_string(
            "catalog/admin/parents.html", {"categories": obj.parents}
        )


@register(ProductKind)
class ProductKindAdmin(CategoryAdmin):
    fieldsets = deepcopy(CategoryAdmin.fieldsets)
    fieldsets[0][1]["fields"] = [
        ("parents", "parent"),
        ("name", "slug", "name_format"),
        "specs_schema",
    ]


@register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ["__str__", "reference"]

    list_filter = ["kind", "line"]

    form = ProductForm

    save_as = True

    autocomplete_fields = ["kind", "line"]

    search_fields = ["reference", "line__name", "specs"]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("kind", "line"),
                    ("reference", "link", "image"),
                    ("specs", "specs_schema"),
                ],
            },
        ),
    ]
