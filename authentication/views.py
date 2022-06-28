from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, filters, views, status
from datetime import datetime
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from authentication.api.serializers import UserViewsetSerializer
from authentication.models import UserProfile
from authentication.api import serializers, permissions
from rest_framework.settings import api_settings
from authentication import models
from rest_framework.authtoken.models import Token
from authentication.authentication_mixins import Authentication 
from django.contrib.sessions.models import Session
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# Create your views here.

class UserToken(Authentication,views.APIView):
    
    def get(self, request, *args,**kwargs):
        
        try:
            user_token = Token.objects.get(
                user = serializers.UserSerializer().Meta.model.objects.filter(username = self.user.username).first()
                )
            return Response({
                'token':user_token.key
            })
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas'
            }, status = status.HTTP_400_BAD_REQUEST)

class UserRegistrationAPI(CreateAPIView):
    """APIView para los registros de usuarios"""
    serializer_class = serializers.RegisterSerializer
    

    def get(self, request, format=None):
        """Devuelve caracteristicas del APIView"""
        apiview = [
            'Metodos HTTP GET,POST,PUT,PATCH,DELETE'
        ]
        return Response({'message':'Api de Registro', 'apiview': apiview})


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        
        name = serializer.validated_data.get('name')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        message = f'Hola { name }'
        send_mail(f'Bienvenido { name }',
        'Creacion de cuenta exitosa',None,
        [email])
        print(serializer.validated_data)
        
        
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token.key, 'username':user.name,'email':user.email}, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class UserViewsets(viewsets.ModelViewSet):
    """APIViewset para los perfiles de usuario"""
    serializer_class = serializers.UserViewsetSerializer
    queryset = UserProfile.objects.all()
    #authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,IsAdminUser)
    
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('^name', 'email',)
    ordering_fields = ('name',)
    
    def list(self, request):
        queryset = UserProfile.objects.all()
        serializer = UserViewsetSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = UserProfile.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.UserViewsetSerializer(user)
        return Response(serializer.data)
    
    
        
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'detail':'Succesful delete'},status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        
class UserLoginApiView(ObtainAuthToken):
    """Crea tokens de autenticacion de usuario"""
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if created:
            return Response(
                {
                'token': token.key,
                'user':user.name,
                'message':'Sucessful login',
                },
                 status= status.HTTP_201_CREATED)
        else:
            all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    if user.id  == int(session_data.get('_auth_user_id')):
                        session.delete()
            
            token.delete()
            token = Token.objects.create(user = user)
            return Response(
                {
                'token': token.key,
                'username':user.name,
                'email':user.email,
                'message':'Sucessful login'},
                 status= status.HTTP_201_CREATED)


    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES