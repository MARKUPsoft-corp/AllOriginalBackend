from rest_framework import serializers
from .models import Product, ProductImage, ProductSpecification, Review, ReviewImage
from categories.serializers import CategorySerializer

class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les spécifications de produits"""
    
    class Meta:
        model = ProductSpecification
        fields = ['id', 'name', 'value', 'is_highlighted', 'display_order']

class ProductImageSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les images de produits"""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'alt_text']

class ProductListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la liste des produits (données limitées)"""
    
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'brand', 'model', 'price', 'discounted_price', 'old_price',
                 'promo', 'category', 'status', 'in_stock', 'is_featured', 'primary_image', 'specs']
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None
    
    def get_specs(self, obj):
        """Format simple des spécifications pour l'affichage dans les cartes produit"""
        highlighted = obj.specifications.filter(is_highlighted=True).order_by('display_order')[:3]
        # Retourner juste les valeurs sous forme de liste de chaînes
        return [f"{spec.name}: {spec.value}" for spec in highlighted]
    
    def get_description(self, obj):
        """Limité à 150 caractères pour les cartes produit"""
        if obj.description and len(obj.description) > 150:
            return obj.description[:147] + '...'
        return obj.description

class ProductDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les détails d'un produit"""
    
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'brand', 'model', 
                 'price', 'discounted_price', 'old_price', 'promo',
                 'category', 'stock', 'status', 'in_stock', 'is_featured', 'is_active',
                 'created_at', 'updated_at', 'images', 'primary_image', 'specifications', 'specs']
    
    def get_primary_image(self, obj):
        """Récupère l'image principale du produit"""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None
        
    def get_specs(self, obj):
        """Format simple des spécifications pour l'affichage dans les cartes produit"""
        highlighted = obj.specifications.filter(is_highlighted=True).order_by('display_order')[:3]
        # Retourner juste les valeurs sous forme de liste de chaînes
        return [f"{spec.name}: {spec.value}" for spec in highlighted]
                 
class ProductCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création/modification d'un produit"""
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'brand', 'model',
                 'price', 'discounted_price', 'old_price', 'promo',
                 'category', 'stock', 'status', 'in_stock', 'is_featured', 'is_active']


class ReviewImageSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les images d'avis"""
    
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'caption']


class ReviewSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les avis clients"""
    images = ReviewImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'author_name', 'author_email', 'rating', 
                 'title', 'comment', 'is_verified', 'created_at', 'images']
        read_only_fields = ['is_verified', 'created_at']


class ReviewSummarySerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour les résumés d'avis"""
    
    class Meta:
        model = Review
        fields = ['id', 'author_name', 'rating', 'title', 'comment', 'is_verified', 'created_at']
        read_only_fields = ['is_verified', 'created_at']
