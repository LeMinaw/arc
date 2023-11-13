# Generated by Django 4.2.7 on 2023-11-12 02:41

import common.utils
import common.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0003_productkind_name_format_alter_category_parent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name="date d'ajout")),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='produit')),
            ],
            options={
                'verbose_name': 'objet',
            },
        ),
        migrations.CreateModel(
            name='TestBench',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_schema', models.JSONField(default=common.utils.make_default_object_schema, encoder=common.utils.JSONSetEncoder, help_text='Schéma des données de test propres à ce type de produits, au format JSONSchema 2020-12.', max_length=1024, validators=[common.validators.JSONSchemaValidator()], verbose_name='schéma des données de test')),
                ('kind', models.OneToOneField(help_text='Type de produit concerné par ces données de test.', on_delete=django.db.models.deletion.CASCADE, related_name='test_bench', to='catalog.productkind', verbose_name='type de produit')),
            ],
            options={
                'verbose_name': "banc d'essai",
                'verbose_name_plural': "bancs d'essais",
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='date de test')),
                ('data', models.JSONField(default=dict, help_text='Spécifications du produit. Elles seront validées par le schéma de spécifications du type de produit sélectionné.', max_length=1024, verbose_name='données de test')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='test', to='inventory.item', verbose_name='objet')),
            ],
            options={
                'verbose_name': 'données de test',
                'verbose_name_plural': 'données de test',
            },
        ),
    ]
