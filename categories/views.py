from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category
from .serializers import CategorySerializer
from products.models import Product
from products.serializers import ProductListSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les catégories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    lookup_field = 'slug'  # Utiliser le slug au lieu de l'ID pour les opérations
    
    def get_permissions(self):
        """Seuls les administrateurs peuvent modifier les catégories"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """
        Récupérer tous les produits d'une catégorie spécifique
        """
        category = self.get_object()
        products = Product.objects.filter(category=category, is_active=True)
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
