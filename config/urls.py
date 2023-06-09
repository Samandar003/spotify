
from django.contrib import admin
from django.urls import path, include
from api.views import getRoutes
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Spotify API",
      default_version='v1',
      description="Swagger Docs for RESTAPI",
      contact=openapi.Contact("Samandar Shoyimov <samandar20527@gmail.com>"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('music.urls')),
    path('api/', include('api.urls')),
    path('route-api', getRoutes),
    path('user/', include('user.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),

] 
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
