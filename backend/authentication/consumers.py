from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from authentication.models import Message

import json

User = get_user_model()

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
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

class ChatView(WebsocketConsumer):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            return super().get(request, *args, **kwargs)

    def connect(self):
        self.chat_room = 'chat_%s' % self.scope['url_route']['kwargs']['chat_room']
        self.room_group_name = 'chat_%s_group' % self.scope['url_route']['kwargs']

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        message_json = json.loads(text_data)
        message = message_json['message']

        # Save message to database
        to_user = User.objects.get(id=self.scope['url_route']['kwargs']['pk'])
        from_user = self.scope["user"]
        message = Message.objects.create(content=message, to=to_user, author=from_user)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_json
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))