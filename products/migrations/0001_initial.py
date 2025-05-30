# Generated by Django 5.2 on 2025-05-04 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nom')),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix')),
                ('discounted_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Prix remisé')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('status', models.CharField(choices=[('in_stock', 'En stock'), ('low_stock', 'Stock faible'), ('out_of_stock', 'Rupture de stock'), ('coming_soon', 'Bientôt disponible')], default='in_stock', max_length=20, verbose_name='Statut')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Mis en avant')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='categories.category', verbose_name='Catégorie')),
            ],
            options={
                'verbose_name': 'Produit',
                'verbose_name_plural': 'Produits',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Image')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Image principale')),
                ('alt_text', models.CharField(blank=True, max_length=100, verbose_name='Texte alternatif')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='Produit')),
            ],
            options={
                'verbose_name': 'Image de produit',
                'verbose_name_plural': 'Images de produits',
                'ordering': ['-is_primary', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('value', models.CharField(max_length=255, verbose_name='Valeur')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='products.product', verbose_name='Produit')),
            ],
            options={
                'verbose_name': 'Spécification',
                'verbose_name_plural': 'Spécifications',
                'ordering': ['name'],
                'unique_together': {('product', 'name')},
            },
        ),
    ]
