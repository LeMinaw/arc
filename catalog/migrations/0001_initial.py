# Generated by Django 4.2.7 on 2023-11-07 14:16

import common.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="nom")),
                (
                    "specs_schema",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Schéma des spécifications propres à cette catégorie de produits, au format JSONSchema 2020-12.",
                        max_length=1024,
                        validators=[common.validators.JSONSchemaValidator()],
                        verbose_name="schéma de spécifications",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="childs",
                        to="catalog.category",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "catégorie",
            },
        ),
        migrations.CreateModel(
            name="Manufacturer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="nom")),
                (
                    "logo_url",
                    models.URLField(
                        blank=True, max_length=256, verbose_name="URL du logo"
                    ),
                ),
            ],
            options={
                "verbose_name": "fabriquant",
            },
        ),
        migrations.CreateModel(
            name="ProductKind",
            fields=[
                (
                    "category_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="catalog.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "type de produit",
                "verbose_name_plural": "types de produits",
            },
            bases=("catalog.category",),
        ),
        migrations.CreateModel(
            name="Line",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="nom")),
                (
                    "manufacturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lines",
                        to="catalog.manufacturer",
                        verbose_name="fabriquant",
                    ),
                ),
            ],
            options={
                "verbose_name": "gamme",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "reference",
                    models.CharField(
                        blank=True,
                        help_text="Référence dans le catalogue du fabriquant",
                        max_length=64,
                        verbose_name="référence",
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True,
                        help_text="URL du produit sur le site du fabriquant",
                        max_length=256,
                        verbose_name="URL",
                    ),
                ),
                (
                    "specs",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Spécifications du produit. Elles seront validées par le schéma de spécifications du type de produit sélectionné.",
                        max_length=1024,
                        verbose_name="spécifications",
                    ),
                ),
                (
                    "line",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="catalog.line",
                        verbose_name="gamme",
                    ),
                ),
                (
                    "kind",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="catalog.productkind",
                        verbose_name="type de produit",
                    ),
                ),
            ],
            options={
                "verbose_name": "produit",
            },
        ),
    ]
