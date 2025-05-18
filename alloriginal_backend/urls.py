"""
URL configuration for alloriginal_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseNotFound
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from .media_serve import serve_media_file

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/categories/', include('categories.urls')),
    path('api/products/', include('products.urls')),
    path('api/accounts/', include('accounts.urls')),
    
    # API documentation
    path('api/docs/', include_docs_urls(title='AllOriginal API', permission_classes=[permissions.AllowAny])),
    
    # Servir les fichiers médias avec notre fonction personnalisée
    re_path(r'^media/(?P<path>.*)$', serve_media_file, name='serve_media'),
]

# Garder cette ligne en commentaire comme référence
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Servir les fichiers statiques uniquement en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
