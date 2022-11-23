import datetime
import json
from typing import Union

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from posts.models import Comment, Post


class WSConsumers(AsyncWebsocketConsumer):
    """
    Async Object for initialization and handling websocket data
    """
    author = None

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.post_id: Union[int, None] = None
        self.post_group_name: Union[str, None] = None

    async def connect(self) -> None:
        """
        Async Method for connect to WebSocket connection
        """
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = 'posts_%s' % self.post_id

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code) -> None:
        """
        Async method for disconnect from WebSocket connections
        """
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def receive(self, text_data: json) -> None:
        """
        Async method for handling receive data and handling it
        """
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

    async def chat_message(self, event: json) -> None:
        """
        Async Method for getting and data
        into the Frontend (with create comment)
        """
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

    async def like_message(self, event: json) -> None:
        """
        Async Method for getting and data  into
        the Frontend (with like message)
        """
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
    def save_message(self, username: str,
                     room: id, message: str) -> Comment:
        """
        Async Method for save comment into DB
        """
        user = get_object_or_404(User, username=username)
        room = get_object_or_404(Post, id=room)

        comment = Comment.objects.create(author=user, post_id=room.id,
                                         text=message)
        return comment

    @sync_to_async
    def add_or_remove_like(self, username: str,
                           comment_id: int) -> int:
        """
        Async method for add or remove like from
        comment into DB
        """
        user = get_object_or_404(User, username=username)
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.likes.prefetch_related().filter(id=user.id).exists():
            comment.likes.remove(user)
            likes_count = comment.likes.all().count()
            return likes_count

        comment.likes.add(user)
        likes_count = comment.likes.all().count()
        return likes_count
