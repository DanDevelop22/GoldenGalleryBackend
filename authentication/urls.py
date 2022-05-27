from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('user-viewset', UserViewsets, basename='user-viewset')

urlpatterns = [
    path('', include(router.urls)),
    path('prueba/', ApiPrueba.as_view())
]

