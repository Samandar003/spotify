
from django.contrib import admin
from django.urls import path, include
from api.views import getRoutes
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('music.urls')),
    path('api/', include('api.urls')),
    path('route-api', getRoutes),
    path('user/', include('user.urls')),
] 
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
