import datetime
import json
from random import randint
from time import sleep

import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


from django.shortcuts import get_object_or_404

from posts.models import Post, Comment


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
        # Leave room group
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author1': "hello"
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.create_new_comment(message)
        print("HEY")
        await self.send(text_data=json.dumps({
            'message': message,
            'author': str(self.author),
            'created': str(datetime.datetime.now().strftime("%a, %d %B, %Y, %H:%M"))
        }))

    @database_sync_to_async
    def create_new_comment(self, text):
        post_id = self.scope['url_route']['kwargs']['post_id']
        post = get_object_or_404(Post, id=post_id)
        self.post_id = post_id
        self.author = post.author
        Comment.objects.create(
            text=text,
            post=post,
            author=post.author
        )
