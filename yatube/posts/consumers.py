import datetime

import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


from django.shortcuts import get_object_or_404

from posts.models import Post, Comment

from django.contrib.auth.models import User


class WSConsumers(AsyncWebsocketConsumer):
    author = None

    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = 'posts_%s' % self.post_id

        # Join room group
        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        comment = await self.save_message(username, room, message)
        print(comment)

        # Send message to room group
        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                "created": datetime.datetime.strftime(comment.created, '%a, %d %B, %Y, %X')[:-3]
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        created = event['created']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'created': created,
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Post.objects.get(id=room)

        comment = Comment.objects.create(author=user, post_id=room.id, text=message)
        self.disconnect(close_code=200)
        return comment
