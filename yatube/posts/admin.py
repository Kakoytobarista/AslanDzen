from typing import Type

from django.contrib import admin
from django.db.models import Model

from enums import BASE_MODEL_ENUM, PostModelEnum, GroupModelEnum, CommentModelEnum, FollowModelEnum
from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.
    """
    list_display = (
        BASE_MODEL_ENUM.PK.value,
        PostModelEnum.TEXT.value,
        PostModelEnum.PUB_DATE.value,
        PostModelEnum.AUTHOR.value,
        PostModelEnum.GROUP.value
    )
    list_editable = (PostModelEnum.AUTHOR.value,)
    search_fields = (PostModelEnum.TEXT.value,)
    list_filter = (PostModelEnum.PUB_DATE.value,)
    empty_value_display = "-empty-"


class GroupAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Group model.
    """
    list_display = (
        GroupModelEnum.TITLE.value,
        GroupModelEnum.SLUG.value,
        GroupModelEnum.DESCRIPTION.value,
    )
    search_fields = ("title",)


class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    """
    list_display = (
        CommentModelEnum.TEXT.value,
    )
    search_fields = (CommentModelEnum.TEXT.value,)


class FollowAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Follow model.
    """
    list_display = (
        FollowModelEnum.USER.value,
        FollowModelEnum.AUTHOR.value,
    )


def register_model_admin(model: Type[Model], admin_class: Type[admin.ModelAdmin]):
    """
    Registers a model with its corresponding admin class.

    Args:
        model (Type[Model]): The Django model class to be registered.
        admin_class (Type[admin.ModelAdmin]): The admin class for the model.
    """
    admin.site.register(model, admin_class)


register_model_admin(Post, PostAdmin)
register_model_admin(Group, GroupAdmin)
register_model_admin(Comment, CommentAdmin)
register_model_admin(Follow, FollowAdmin)
