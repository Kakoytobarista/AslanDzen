import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404

from posts.models import Comment
from posts.models import Post


class CommentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = 'post_%s' % self.post_id

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
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        comment = text_data_json['text']
        new_comment = await self.create_new_comment(comment)
        data = {'author': new_comment.author.username,
                'created_at': new_comment.created_at.strftime('%Y-%m-%d %H:%m'),
                'text': new_comment.text}
        # Send message to room group
        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'new_comment',
                'message': data
            }
        )

    # Receive message from room group
    async def new_comment(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_new_comment(self, text):
        post = get_object_or_404(Post, self.post_id)
        new_comment = Comment.objects.create(
            author=self.scope['user'],
            text=text,
            post=post
        )
        return new_comment
