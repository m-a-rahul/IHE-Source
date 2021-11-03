from django.urls import path
from .views import CreateUpdateUserDetails, GetUserDetails

app_name = 'user_details'

urlpatterns = [
    path('get/', GetUserDetails.as_view()),
    path('create_update/', CreateUpdateUserDetails.as_view()),
]
