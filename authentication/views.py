import email
from re import search
from unicodedata import name
from urllib import request, response
from django.shortcuts import render
from rest_framework import viewsets, filters, views, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from authentication.api import serializers, permissions
from rest_framework.settings import api_settings
from authentication import models
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
# Create your views here.



class UserRegistrationAPI(views.APIView):
    """APIView para los registros de usuarios"""
    serializer_class= serializers.RegisterSerializer

    

    def get(self, request, format=None):
        """Devuelve caracteristicas del APIView"""
        apiview = [
            'Metodos HTTP GET,POST,PUT,PATCH,DELETE'
        ]
        return Response({'message':'Hola', 'apiview': apiview})


    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hola { name }'
            serializer.save()
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserViewsets(viewsets.ModelViewSet):
    """APIViewset para los perfiles de usuario"""
    serializer_class = serializers.UserSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

        

class UserLoginApiView(ObtainAuthToken):
    """Crea tokens de autenticacion de usuario"""
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'user':user.name})

    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES