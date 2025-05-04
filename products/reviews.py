from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from .models import Product

class Review(models.Model):
    """Modèle pour les avis clients sur les produits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Produit")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews', verbose_name="Utilisateur")
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
