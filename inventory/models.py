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
        related_name="stock",
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
    specs = JSONField(
        max_length=1024,
        blank=True,
        default=dict,
        verbose_name="spécifications",
        help_text=(
            "Spécifications de l'objet. Elles seront validées par le schéma de "
            "spécifications d'objets du type de produit sélectionné."
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
    out_date = DateTimeField(
        blank=True,
        null=True,
        verbose_name="date de sortie de stock",
    )

    class Meta:
        get_latest_by = "mod_date"
        verbose_name = "objet"

    def __str__(self):
        if name_format := self.product.kind.item_name_format:
            return name_format.format(
                **(self.product.specs | self.specs), PRODUCT=str(self.product)
            )
        return str(self.product)

    def save(self, *args, **kwargs):
        # We need to manually call clean because DRF does not do this anymore since
        # v3.0, and does not provide any reasonable way to do this kind of validation
        self.clean()

        super().save(*args, **kwargs)

    def clean(self):
        self._validate_specs()

    def _validate_specs(self):
        validator = JSONSchemaValidator(self.product.kind.item_specs_schema)

        try:
            validator(self.specs)
        except ValidationError as e:
            raise ValidationError({"specs": e.message}) from e

    @property
    def test_bench(self):
        return getattr(self.product.kind, "test_bench", None)


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

    def save(self, *args, **kwargs):
        # If a test does not contain data anymore, the whole object can be deleted
        if not self.data:
            if self.pk is not None:
                self.delete()

        else:
            # We need to manually call clean because DRF does not do this anymore since
            # v3.0, and does not provide any reasonable way to do this kind of
            # validation
            self.clean()

            super().save(*args, **kwargs)

    def clean(self):
        self._validate_test_data()

    def _validate_test_data(self):
        if not (bench := self.item.test_bench):
            raise ValidationError(
                "Aucun banc d'essai défini pour le type de produit "
                f"{self.item.product.kind}"
            )

        validator = JSONSchemaValidator(bench.data_schema)

        try:
            validator(self.data)
        except ValidationError as e:
            raise ValidationError({"data": e.message}) from e
