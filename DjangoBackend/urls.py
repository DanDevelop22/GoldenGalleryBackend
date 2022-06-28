from django.contrib import admin

from django.urls import path, include, re_path 
from rest_framework.routers import DefaultRouter


from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls', namespace='rest_framework')),
    path('', include('authentication.urls')),
    path('refresh-token',views.UserToken.as_view(), name='refresh_token')
]
