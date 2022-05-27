from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.api import serializers, permissions
from authentication import models


class ApiPrueba(APIView):
    """Esta api es de prueba para llamarla en flutter"""
    
    def get(self, request):
        return Response({'data': 'Probando Apis en Flutter'}, status=status.HTTP_200_OK)

class UserViewsets(viewsets.ModelViewSet):
    """APIViewset para los perfiles de usuario"""
    serializer_class = serializers.UserSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)