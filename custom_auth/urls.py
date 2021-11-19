from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from custom_auth.views import CreateUser, CurrentUser

app_name = 'custom_auth'

urlpatterns = [
    path('register/', CreateUser.as_view()),
    path('login/', obtain_jwt_token),
    path('current_user/', CurrentUser.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
