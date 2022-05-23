import email
from re import search
from urllib import request, response
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from authentication.api import serializers, permissions
from authentication import models
# Create your views here.


class UserViewsets(viewsets.ModelViewSet):
    """APIViewset para los perfiles de usuario"""
    serializer_class = serializers.UserSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)