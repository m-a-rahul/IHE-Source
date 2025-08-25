from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from src.settings import ADMIN_URL

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('user-details/', include('user_details.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
