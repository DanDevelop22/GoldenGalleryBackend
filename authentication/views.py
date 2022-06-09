import email
from re import search
from unicodedata import name
from urllib import request, response
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, filters, views, status

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from authentication.api.serializers import UserSerializer
from authentication.models import UserProfile
from authentication.api import serializers, permissions
from rest_framework.settings import api_settings
from authentication import models
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
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
            email = serializer.validated_data.get('email')
            message = f'Hola { name }'
            send_mail(f'Bienvenido { name }',
            'Creacion de cuenta exitosa',None,
            [email])
            serializer.save()
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserViewsets(viewsets.ModelViewSet):
    """APIViewset para los perfiles de usuario"""
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile,IsAuthenticated)
    
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('^name', 'email',)
    ordering_fields = ('name',)
    
    def list(self, request):
        queryset = UserProfile.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = UserProfile.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
    def perform_create(self, serializer):
        serializer.save(name=self.request.user)
        
class UserLoginApiView(ObtainAuthToken):
    """Crea tokens de autenticacion de usuario"""
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'user':user.name})

    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES