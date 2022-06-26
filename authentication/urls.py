from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()
router.register('user-viewset', views.UserViewsets, basename='user-viewset')

urlpatterns = [
    path('', include(router.urls)),

    
]

