
from django.contrib import admin
from django.urls import path, include
from api.views import getRoutes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('music.urls')),
    path('api/', include('api.urls')),
    path('route-api', getRoutes),
]
