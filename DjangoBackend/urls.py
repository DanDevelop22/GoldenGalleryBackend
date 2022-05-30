from django.contrib import admin

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.UserLoginApiView.as_view()),
    path('register/',views.UserRegistrationAPI.as_view()),
    
    path('api/auth/', include('authentication.urls'))
]
