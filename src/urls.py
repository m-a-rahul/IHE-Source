from django.contrib import admin
from django.urls import path, include
from decouple import config

urlpatterns = [
    path(config('ADMIN_URL'), admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
]
