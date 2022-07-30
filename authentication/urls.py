from django.urls import path, include
from rest_framework.routers import DefaultRouter
from DjangoBackend import settings
from authentication import views

router = DefaultRouter()
router.register('user-viewset', views.UserViewsets, basename='user-viewset')
router.register('cuadro-viewset',views.CuadroViewset,basename='cuadro-viewset')
router.register('usercuadro-viewset',views.UserCuadroViewset,basename='usercuadro-viewset')
router.register('on_sell-viewset',views.CuadroOnSellViewset,basename='on_sell-viewset')
urlpatterns = [
    path('', include(router.urls)),
    path('login/',views.UserLoginApiView.as_view()),
    path('register/',views.UserRegistrationAPI.as_view()),
    path('refresh-token',views.UserToken.as_view(), name='refresh_token')
]

