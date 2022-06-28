import email
from rest_framework import serializers
from authentication import models

class UserSerializer(serializers.ModelSerializer): 
    """Serializa objetos de perfil de usuario"""
    class Meta:
        model = models.UserProfile
        fields = ('id','email','password')
        extra_keywords = {
            'password':{
                'write_only': True,
                'style':{'input_style':'password'}
            }
        }     

    def create(self, validated_data):
        """Crear y devolver un nuevo usuario"""
        user = models.UserProfile.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']

        )
        print(user)
        return user
    
    def update(self, instance, validated_data):
        """Actualiza cuenta de usuario"""

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data) 


class RegisterSerializer(serializers.ModelSerializer):
    """Serializador para el registro"""
    class Meta:
        model = models.UserProfile
        fields = ('id','name','email','password')
        extra_keywords = {
            'password':{
                'write_only': True,
                'style':{'input_style':'password'}
            }
        }     

    def create(self, validated_data):
        """Crear y devolver un nuevo usuario"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']

        )

        return user
    
    
class UserViewsetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password','is_staff','is_active')
        extra_keywords = {
            'password':{
                'write_only': True,
                'style':{'input_style':'password'}
            }
        }
        
    def create(self, validated_data):
        """Crear y devolver un nuevo usuario"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name = validated_data['name'],
            password=validated_data['password']

        )

        return user
    
    def update(self, instance, validated_data):
        """Actualiza cuenta de usuario"""

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data) 