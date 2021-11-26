from django.urls import path
from user_details.views import CreateUpdateUserDetails, CreateHospitalStaff, GetHospitalStaffDetails

app_name = 'user_details'

urlpatterns = [
    path('create_update/', CreateUpdateUserDetails.as_view()),
    path('upload/', CreateHospitalStaff.as_view()),
    path('getstaff/', GetHospitalStaffDetails.as_view()),
]
