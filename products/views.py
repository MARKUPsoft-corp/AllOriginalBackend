from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import Product, ProductImage, ProductSpecification
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, 
    ProductCreateSerializer, ProductImageSerializer,
    ProductSpecificationSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les produits
    """
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'created_at', 'category']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        elif self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'add_image', 'delete_image', 'add_specification', 'delete_specification']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filtrage par catégorie
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filtrage par statut
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filtrage par prix min/max
        price_min = self.request.query_params.get('price_min', None)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
            
        price_max = self.request.query_params.get('price_max', None)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        
        # Produits mis en avant
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Produits actifs seulement (pour les non-admin)
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
            
        return queryset
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def add_image(self, request, slug=None):
        """
        Ajouter une image à un produit
        """
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='images/(?P<image_id>[^/.]+)')
    def delete_image(self, request, slug=None, image_id=None):
        """
        Supprimer une image d'un produit
        """
        product = self.get_object()
        try:
            image = ProductImage.objects.get(id=image_id, product=product)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def add_specification(self, request, slug=None):
        """
        Ajouter une spécification à un produit
        """
        product = self.get_object()
        serializer = ProductSpecificationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='specifications/(?P<spec_id>[^/.]+)')
    def delete_specification(self, request, slug=None, spec_id=None):
        """
        Supprimer une spécification d'un produit
        """
        product = self.get_object()
        try:
            spec = ProductSpecification.objects.get(id=spec_id, product=product)
            spec.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductSpecification.DoesNotExist:
            return Response({"detail": "Specification not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Récupérer les produits mis en avant
        """
        products = Product.objects.filter(is_featured=True, is_active=True)
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Recherche avancée de produits
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query)
        ).filter(is_active=True).distinct()
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
