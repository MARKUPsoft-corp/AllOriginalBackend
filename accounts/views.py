from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import UserProfile
from .serializers import UserSerializer, UserCreateSerializer, UserProfileSerializer, LoginSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les utilisateurs (admin uniquement)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint pour le profil utilisateur courant
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Mise à jour des champs de l'utilisateur si nécessaire
        user_data = {}
        if 'first_name' in request.data:
            user_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data:
            user_data['last_name'] = request.data['last_name']
        
        if user_data:
            user_serializer = UserSerializer(request.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    """
    API endpoint pour l'inscription des utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Création d'un token pour l'utilisateur
        token, created = Token.objects.get_or_create(user=user)
        
        # Auto-login après inscription
        login(request, user)
        
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    API endpoint pour la connexion des utilisateurs
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            request, 
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user, context={'request': request}).data,
                'token': token.key
            })
        return Response(
            {"detail": "Email ou mot de passe invalide"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    """
    API endpoint pour la déconnexion des utilisateurs
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Suppression du token
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        
        # Déconnexion de la session Django
        logout(request)
        
        return Response({"detail": "Déconnecté avec succès"}, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    """
    API endpoint pour récupérer l'utilisateur actuellement connecté
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
