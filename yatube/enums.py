from enum import Enum


class AboutPage(Enum):
    AUTHOR = 'about/author.html'
    TECH = 'about/tech.html'

class AboutTitle(Enum):
    AUTHOR = 'About Author'
    TECH = 'Tech'


class CreatedModelEnum(Enum):
    PUB_DATE_VERBOSE_NAME = 'Creation Date'


class HtmlPathEnum(Enum):
    INDEX_PAGE = 'posts/index.html'
    GROUP_PAGE = 'posts/group_list.html'
    PROFILE_PAGE = 'posts/profile.html'
    POST_DETAIL_PAGE = 'posts/post_detail.html'
    POST_CREATE_EDIT_PAGE = 'posts/create_post.html'
    FOLLOW_PAGE = 'posts/follow.html'


class BASE_MODEL_ENUM(Enum):
    PK = 'pk'
    PUB_DATE = 'pub_date'


class UserModelEnum(BASE_MODEL_ENUM):
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    USERNAME = 'username'
    EMAIL = 'email'


class GroupModelEnum(BASE_MODEL_ENUM):
    DESCRIPTION = 'description'
    TITLE = 'title'
    SLUG = 'slug'


class PostModelEnum(BASE_MODEL_ENUM):
    TEXT = 'text'
    AUTHOR = 'author'
    GROUP = 'group'
    IMAGE = 'image'

class CommentModelEnum(Enum):
    TEXT = 'text'


class FollowModelEnum(Enum):
    USER = 'user'
    AUTHOR = 'author'
