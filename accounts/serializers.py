from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les profils utilisateurs"""
    
    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'address', 'city', 'postal_code', 
                 'country', 'photo', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs"""
    
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 
                 'is_staff', 'date_joined', 'profile']
        read_only_fields = ['is_active', 'is_staff', 'date_joined']

class UserCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création d'un utilisateur"""
    
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs
    
    def create(self, validated_data):
        # Supprimer password2 car il n'est pas nécessaire pour la création de l'utilisateur
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Créer le profil utilisateur
        UserProfile.objects.create(user=user)
        
        return user

class LoginSerializer(serializers.Serializer):
    """Sérialiseur pour l'authentification"""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
