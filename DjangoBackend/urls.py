from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('login/',views.UserLoginApiView.as_view()),
    path('register/',views.UserRegistrationAPI.as_view()),
    path('', include(router.urls))
=======
    path('api/auth/', include('authentication.urls'))
>>>>>>> 62e1e6ead1066e61cd32034f3c3bda9fba7c6a9d
]
