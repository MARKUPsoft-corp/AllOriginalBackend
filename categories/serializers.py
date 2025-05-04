from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les catégories"""
    
    class Meta:
        model = Category
        fields = '__all__'
