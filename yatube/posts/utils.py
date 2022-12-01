from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


def get_users(request, username):
    follower = get_object_or_404(User, username=request.user)
    following = get_object_or_404(User, username=username)
    return follower, following
