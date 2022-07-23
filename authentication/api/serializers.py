from rest_framework import serializers

from authentication import models
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer): 
    """Serializa objetos de perfil de usuario"""
    cuadros = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='cuadro-viewset'
        )

    class Meta:
        model = models.UserProfile
        fields = ('id','email','password','cuadros')
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
    
    paint = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        
        )
    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password','is_staff','is_active','paint')
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

class UserCuadroSerializer(serializers.ModelSerializer):
    #img = serializers.Field(source='img.url')
    img_url = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(many=False,
        read_only=True,)
    class Meta:
        model = models.Paint
        fields = ('name','img_url','user')

    def get_img_url(self, cuadro):
        request = self.context.get('request')
        img_url = cuadro.img.url
        return request.build_absolute_uri(img_url)


    def create(self, validated_data):
        """Crear y devolver un nuevo usuario"""
        cuadro = models.Cuadro.objects.create(
            name=validated_data['name'],
            img=validated_data['img'],
            

        )
        print(cuadro)
        return cuadro

class CuadroSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = models.Paint
        fields = ('name','img')

    


    def create(self, validated_data):
        """Crear y devolver un nuevo usuario"""
        cuadro = models.Cuadro.objects.create(
            name=validated_data['name'],
            img=validated_data['img'],
            

        )
        print(cuadro)
        return cuadro