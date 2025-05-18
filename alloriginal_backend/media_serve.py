from django.http import FileResponse
from django.conf import settings
import os

def serve_media_file(request, path):
    """
    Fonction personnalisée pour servir les fichiers média avec les en-têtes CORS appropriés
    """
    # Construit le chemin complet du fichier
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Vérifie si le fichier existe
    if not os.path.exists(file_path):
        return HttpResponseNotFound("Fichier non trouvé")
    
    # Crée une réponse avec le fichier
    response = FileResponse(open(file_path, 'rb'))
    
    # Ajoute les en-têtes CORS nécessaires
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept"
    
    return response
