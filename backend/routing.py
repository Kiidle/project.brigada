from django.urls import path

from authentication.consumers import ChatConsumer, ChatView

websocket_urlpatterns = [
    path("ws/test/", ChatConsumer.as_asgi()),
    path("chats/<int:pk>/", ChatView.as_asgi(), name="chat"),
]