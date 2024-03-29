# Generated by Django 4.2.7 on 2024-01-12 01:16
# MANUALLY EDITED

from django.db import migrations, models
from django.utils.text import slugify


def populate_categories_slug_field(apps, schema_editor):
    for category in apps.get_model("catalog", "category").objects.all():
        category.slug = slugify(category.name)
        category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, max_length=32, unique=True, verbose_name='identifiant'),
            preserve_default=False,
        ),
        migrations.RunPython(populate_categories_slug_field, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=False, max_length=32, unique=True, verbose_name='identifiant'),
            preserve_default=False,
        ),
    ]

