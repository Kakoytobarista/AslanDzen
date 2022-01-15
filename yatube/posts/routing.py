from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'posts/(?P<post_id>/d+)/$', consumers.CommentsConsumer.as_asgi()),
]
