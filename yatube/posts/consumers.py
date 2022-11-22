import datetime

import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


from posts.models import Post, Comment

from django.contrib.auth.models import User


class WSConsumers(AsyncWebsocketConsumer):
    author = None

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.post_id = None
        self.post_group_name = None

    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = 'posts_%s' % self.post_id

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')
        if data.get('comment_id'):
            likes_count = await self.add_or_remove_like(username, data['comment_id'])
            await self.channel_layer.group_send(
                self.post_group_name,
                {
                    'type': 'like_message',
                    'username': username,
                    'comment_id': data.get('comment_id'),
                    'likes_count': str(likes_count),
                }
            )
            return

        message = data.get('message')
        room = data.get('room')

        comment = await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'created': datetime.datetime.strftime(comment.created, '%a, %d %B, %Y, %X')[:-3],
                'comment_id': comment.id,
            }
        )

    async def chat_message(self, event):
        comment_id = event.get('comment_id')
        username = event.get('username')

        message = event.get('message')
        created = event.get('created')
        type_ = event.get('type')

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'created': created,
            'comment_id': comment_id,
            'type': type_
        }))

    async def like_message(self, event):
        username = event.get('username')
        type_ = event.get('type')
        comment_id = event.get('comment_id')
        likes_count = event.get('likes_count')

        await self.send(text_data=json.dumps({
            'type': type_,
            'username': username,
            'comment_id': comment_id,
            'likes_count': likes_count
            }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Post.objects.get(id=room)

        comment = Comment.objects.create(author=user, post_id=room.id, text=message)
        return comment

    @sync_to_async
    def add_or_remove_like(self, username, comment_id):
        user = User.objects.get(username=username)
        comment = Comment.objects.get(id=comment_id)
        if user in comment.likes.prefetch_related():
            comment.likes.remove(user)
            likes_count = len(comment.likes.all())
            return likes_count

        comment.likes.add(user)
        likes_count = len(comment.likes.all())
        return likes_count
