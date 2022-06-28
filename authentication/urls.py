from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()
router.register('user-viewset', views.UserViewsets, basename='user-viewset')

urlpatterns = [
    path('', include(router.urls)),
    path('login/',views.UserLoginApiView.as_view()),
    path('register/',views.UserRegistrationAPI.as_view()),
]

