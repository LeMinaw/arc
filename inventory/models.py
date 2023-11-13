from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    BooleanField,
    DateTimeField,
    ForeignKey,
    JSONField,
    Model,
    OneToOneField,
)
from django.templatetags.l10n import localize

from common.utils import JSONSetEncoder, make_default_object_schema
from common.validators import JSONSchemaValidator


class Item(Model):
    product = ForeignKey(
        "catalog.Product",
        on_delete=CASCADE,
        verbose_name="produit",
    )
    in_stock = BooleanField(
        default=True,
        verbose_name="en stock",
        help_text=(
            "Plutôt que de supprimer un article, il est préférable de le marquer hors "
            "stock."
        ),
    )
    add_date = DateTimeField(
        auto_now_add=True,
        verbose_name="date d'ajout",
    )
    mod_date = DateTimeField(
        auto_now=True,
        verbose_name="date de modification",
    )

    class Meta:
        verbose_name = "objet"

    def __str__(self):
        return str(self.product)


class TestBench(Model):
    kind = OneToOneField(
        "catalog.ProductKind",
        on_delete=CASCADE,
        related_name="test_bench",
        verbose_name="type de produit",
        help_text="Type de produit concerné par ces données de test.",
    )
    data_schema = JSONField(
        max_length=1024,
        validators=[JSONSchemaValidator()],
        default=make_default_object_schema,
        encoder=JSONSetEncoder,
        verbose_name="schéma des données de test",
        help_text=(
            "Schéma des données de test propres à ce type de produits, au format "
            "JSONSchema 2020-12."
        ),
    )

    class Meta:
        verbose_name = "banc d'essai"
        verbose_name_plural = "bancs d'essais"

    def __str__(self):
        return str(self.kind)


class Test(Model):
    item = OneToOneField(
        "Item",
        on_delete=CASCADE,
        related_name="test",
        verbose_name="objet",
    )
    date = DateTimeField(
        auto_now=True,
        verbose_name="date de test",
    )
    data = JSONField(
        max_length=1024,
        default=dict,
        verbose_name="données de test",
        help_text=(
            "Spécifications du produit. Elles seront validées par le schéma de "
            "spécifications du type de produit sélectionné."
        ),
    )

    class Meta:
        verbose_name = "données de test"
        verbose_name_plural = "données de test"

    def __str__(self):
        return f"{self.item} - {localize(self.date)}"  # :%d/%m/%Y, %H:%M

    def clean(self):
        self._validate_test_data()

    def _validate_test_data(self):
        if not (bench := getattr(self.item.product.kind, "test_bench", None)):
            raise ValidationError(
                f"Aucun banc d'essai défini pour le type de produit {self.kind}"
            )

        validator = JSONSchemaValidator(bench.data_schema)

        try:
            validator(self.data)
        except ValidationError as e:
            raise ValidationError({"data": e.message}) from e
