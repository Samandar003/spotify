
from django.contrib import admin
from django.urls import path, include
from api.views import getRoutes
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('music.urls')),
    path('api/', include('api.urls')),
    path('route-api', getRoutes),
] 
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
