from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    ForeignKey,
    ImageField,
    JSONField,
    Model,
    SlugField,
    URLField,
)

from common.utils import JSONSetEncoder, make_default_object_schema
from common.validators import JSONSchemaValidator


class Manufacturer(Model):
    name = CharField(
        max_length=32,
        verbose_name="nom",
    )
    logo_url = URLField(
        max_length=256,
        blank=True,
        verbose_name="URL du logo",
    )

    class Meta:
        verbose_name = "fabriquant"

    def __str__(self):
        return self.name


class Line(Model):
    manufacturer = ForeignKey(
        "Manufacturer",
        on_delete=CASCADE,
        related_name="lines",
        verbose_name="fabriquant",
    )
    name = CharField(
        max_length=32,
        verbose_name="nom",
    )

    class Meta:
        verbose_name = "gamme"

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class Category(Model):
    parent = ForeignKey(
        "self",
        limit_choices_to={"productkind__isnull": True},
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="childs",
        verbose_name="parent",
    )
    name = CharField(
        max_length=32,
        verbose_name="nom",
    )
    slug = SlugField(
        max_length=32,
        unique=True,
        verbose_name="identifiant",
    )
    specs_schema = JSONField(
        max_length=1024,
        validators=[JSONSchemaValidator()],
        default=make_default_object_schema,
        encoder=JSONSetEncoder,
        verbose_name="schéma de spécifications",
        help_text=(
            "Schéma des spécifications propres à cette catégorie de produits, au "
            "format JSONSchema 2020-12."
        ),
    )

    class Meta:
        verbose_name = "catégorie"

    def __str__(self):
        return f"{self.name}"

    @property
    def parents(self):
        return list(reversed(list(self._move_up_hierarchy())))

    def coalesce_specs_schema(self):
        schema = make_default_object_schema()

        for item in self.parents:
            if properties := item.specs_schema.get("properties"):
                schema["properties"] |= properties
            if required := item.specs_schema.get("required"):
                schema["required"] |= set(required)
            if item.specs_schema.get("additionalProperties") is True:
                schema["additionalProperties"] = True

        return schema

    def _move_up_hierarchy(self):
        yield (item := self)
        while item := item.parent:
            yield item


class ProductKind(Category):
    name_format = CharField(
        max_length=128,
        verbose_name="format du nom",
        help_text="Gabarit Python spécifiant le nom des produits.",
    )

    class Meta:
        verbose_name = "type de produit"
        verbose_name_plural = "types de produits"


class Product(Model):
    kind = ForeignKey(
        "ProductKind",
        on_delete=CASCADE,
        related_name="products",
        verbose_name="type de produit",
    )
    line = ForeignKey(
        "Line",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        verbose_name="gamme",
    )
    reference = CharField(
        max_length=64,
        blank=True,
        verbose_name="référence",
        help_text="Référence dans le catalogue du fabriquant",
    )
    link = URLField(
        max_length=256,
        blank=True,
        verbose_name="URL",
        help_text="URL du produit sur le site du fabriquant",
    )
    image = ImageField(
        upload_to="products",
        blank=True,
        verbose_name="image",
        help_text="Image d'illustration du produit.",
    )
    specs = JSONField(
        max_length=1024,
        blank=True,
        default=dict,
        verbose_name="spécifications",
        help_text=(
            "Spécifications du produit. Elles seront validées par le schéma de "
            "spécifications du type de produit sélectionné."
        ),
    )

    class Meta:
        verbose_name = "produit"

    def __str__(self):
        if self.line:
            return f"{self.line} - {self.name}"
        return self.name

    @property
    def name(self):
        return self.kind.name_format.format(**self.specs)

    def get_specs_schema(self):
        return self.kind.coalesce_specs_schema()

    def clean(self):
        self._validate_specs()

    def _validate_specs(self):
        validator = JSONSchemaValidator(self.get_specs_schema())

        try:
            validator(self.specs)
        except ValidationError as e:
            raise ValidationError({"specs": e.message}) from e
