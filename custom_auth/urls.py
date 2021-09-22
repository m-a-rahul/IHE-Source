from django.urls import path, include
from .views import UserList
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'custom_auth'

urlpatterns = [
    path('register/', UserList.as_view()),
    path('login/', obtain_jwt_token),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
