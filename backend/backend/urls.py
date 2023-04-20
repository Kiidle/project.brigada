from django.contrib import admin
from django.urls import include, path

from routing import websocket_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("authentication.urls")),
    path('', include(websocket_urlpatterns)),
]