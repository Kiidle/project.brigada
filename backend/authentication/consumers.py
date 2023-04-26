from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from authentication.models import Message
from django.db.models import Q

import json

User = get_user_model()

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()

class ChatViewWrapper(TemplateView):
    template_name = "chats/chat.html"

    def form_valid(self, form):
        # Handle valid form submission
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form submission
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        # Handle the form submission here
        return redirect('chat', pk=kwargs['pk'])

class ChatRoom(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'room_name'
        self.room_group_name = f'chat_{self.room_name}'

        # Gruppe dem Channel hinzufügen
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # WebSocket-Verbindung akzeptieren
        await self.accept()

    async def disconnect(self, close_code):
        # Gruppe aus dem Channel entfernen
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        author = text_data_json['author']
        to = text_data_json['to']
        content = text_data_json['content']

        if to == str(self.scope['user'].id):
            # Get the channel layer
            channel_layer = get_channel_layer()

            # Send the message to the intended recipient
            await channel_layer.send(
                f'chat_{to}',
                {
                    'type': 'chat_message',
                    'author': author,
                    'content': content
                }
            )

    async def chat_message(self, event):
        # Hier kannst du die Nachricht an den Client senden
        await self.send(json.dumps({
            'author': event['author'],
            'to': event['to'],
            'content': event['content']
        }))
