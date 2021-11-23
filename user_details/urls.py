from django.urls import path
from user_details.views import CreateUpdateUserDetails, GetUserDetails, CreateHospitalStaff, GetHospitalStaffDetails

app_name = 'user_details'

urlpatterns = [
    path('get/', GetUserDetails.as_view()),
    path('create_update/', CreateUpdateUserDetails.as_view()),
    path('upload/', CreateHospitalStaff.as_view()),
    path('getstaff/', GetHospitalStaffDetails.as_view()),
]
