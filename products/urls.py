from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .reviews_viewset import ReviewViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
