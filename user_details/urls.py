from django.urls import path, include
from .views import Patient, Hospital

app_name = 'user_details'

urlpatterns = [
    path('patient/', Patient.as_view()),
    path('hospital/', Hospital.as_view()),
]
