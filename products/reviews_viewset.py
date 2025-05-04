from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Review
from .serializers import ReviewSerializer, ReviewSummarySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """API endpoint pour les avis clients"""
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter(is_approved=True)
    
    def get_permissions(self):
        """Définir les permissions en fonction de l'action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Créer un nouvel avis client"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        """Récupérer les avis par produit (identifié par slug)"""
        product_slug = request.query_params.get('product_slug', None)
        if not product_slug:
            return Response({'error': 'Le paramètre product_slug est requis'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            return Response({'error': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)
            
        reviews = self.queryset.filter(product=product).order_by('-created_at')
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
