from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from categories.models import Category

class Product(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'En stock'),
        ('low_stock', 'Stock faible'),
        ('out_of_stock', 'Rupture de stock'),
        ('coming_soon', 'Bientôt disponible'),
    ]
    
    # Informations de base
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Catégorie")
    
    # Informations de marque
    brand = models.CharField(max_length=100, verbose_name="Marque", default="Générique")
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modèle")
    
    # Prix et promotions
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix actuel")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix original")
    
    # Stock et disponibilité
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock', verbose_name="Statut")
    
    # Options
    is_featured = models.BooleanField(default=False, verbose_name="Mis en avant")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def promo(self):
        """Indique si le produit est en promotion"""
        return self.original_price is not None and self.original_price > self.price
    
    @property
    def discounted_price(self):
        """Retourne le prix remisé (pour compatibilité avec le code existant)"""
        return self.price if self.promo else None
    
    @property
    def old_price(self):
        """Retourne l'ancien prix (pour compatibilité avec le code existant)"""
        return self.original_price
        
    @property
    def in_stock(self):
        """Indique si le produit est en stock"""
        return self.status in ['in_stock', 'low_stock'] and self.stock > 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produit")
    image = models.ImageField(upload_to='products/', verbose_name="Image")
    is_primary = models.BooleanField(default=False, verbose_name="Image principale")
    alt_text = models.CharField(max_length=100, blank=True, verbose_name="Texte alternatif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Image de produit"
        verbose_name_plural = "Images de produits"
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"Image pour {self.product.name} ({self.id})"

class SpecificationType(models.Model):
    """Type de spécification prédéfini pour éviter les doublons"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    display_name = models.CharField(max_length=100, verbose_name="Nom d'affichage")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Type de spécification"
        verbose_name_plural = "Types de spécifications"
        ordering = ['name']
    
    def __str__(self):
        return self.display_name

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications', verbose_name="Produit")
    # Conserver le champ name original pour la rétrocompatibilité
    name = models.CharField(max_length=100, verbose_name="Nom")
    # Ajouter spec_type comme champ nullable pour permettre une migration en douceur
    spec_type = models.ForeignKey(SpecificationType, on_delete=models.CASCADE, verbose_name="Type de spécification", null=True, blank=True)
    value = models.CharField(max_length=255, verbose_name="Valeur")
    is_highlighted = models.BooleanField(default=False, verbose_name="Spécification mise en avant")
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Spécification"
        verbose_name_plural = "Spécifications"
        ordering = ['display_order', 'name']
        # Temporairement, n'utiliser que product et name
        unique_together = ('product', 'name')
    
    def __str__(self):
        if self.spec_type:
            return f"{self.spec_type.display_name}: {self.value} ({self.product.name})"
        return f"{self.name}: {self.value} ({self.product.name})"


class Review(models.Model):
    """Modèle pour les avis clients sur les produits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Produit")
    author_name = models.CharField(max_length=100, verbose_name="Nom de l'auteur")
    author_email = models.EmailField(verbose_name="Email de l'auteur", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Note (1-5)")
    title = models.CharField(max_length=100, verbose_name="Titre de l'avis", blank=True)
    comment = models.TextField(verbose_name="Commentaire")
    is_verified = models.BooleanField(default=False, verbose_name="Achat vérifié")
    is_approved = models.BooleanField(default=True, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    class Meta:
        verbose_name = "Avis client"
        verbose_name_plural = "Avis clients"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Avis de {self.author_name} sur {self.product.name}"


class ReviewImage(models.Model):
    """Images associées aux avis clients"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images', verbose_name="Avis")
    image = models.ImageField(upload_to='reviews/', verbose_name="Image")
    caption = models.CharField(max_length=100, blank=True, verbose_name="Légende")
    
    class Meta:
        verbose_name = "Image d'avis"
        verbose_name_plural = "Images d'avis"
        
    def __str__(self):
        return f"Image pour avis #{self.review.id}"
