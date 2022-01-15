from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/posts/<int:post_id>/', consumers.CommentsConsumer.as_asgi()),
]
