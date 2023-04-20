from django.urls import path

from authentication.consumers import ChatConsumer, ChatRoom

websocket_urlpatterns = [
    path("ws/test/", ChatConsumer.as_asgi()),
    path("chats", ChatRoom.as_asgi())
]