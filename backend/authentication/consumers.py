from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from authentication.models import Message

import json

User = get_user_model()

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()


class ChatViewWrapper(TemplateView):
    template_name = "chats/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = kwargs.get('pk')
        user = User.objects.get(pk=pk)
        context['user'] = user

        message_ids = []
        for message in self.request.user.sent_messages.all():
            message_ids.append(message.id)
        for message in self.request.user.received_messages.all():
            message_ids.append(message.id)

        message_ids = sorted(message_ids)

        messages = []
        for message_id in message_ids:
            message = Message.objects.get(id=message_id)
            messages.append(message)

            context["messages"] = messages

        context["users"] = User.objects.order_by('first_name', 'last_name')

        print(context)

        return context

    def post(self, request, *args, **kwargs):
        message_content = request.POST.get('message')
        to_user = User.objects.get(id=kwargs.get('pk'))
        from_user = request.user
        message = Message.objects.create(content=message_content, to=to_user, author=from_user)
        return redirect(request.path)


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
            # Hier kannst du die Nachricht verarbeiten und entsprechend reagieren

            # Beispiel: Nachricht an alle im Raum senden
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'author': author,
                    'to': to,
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
