from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Name")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.title

class Post(CreatedModel):
    text = models.TextField(verbose_name="Post Text",
                            help_text='This field is for the text of the post, '
                                      'it has no character limits.')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts",
                               verbose_name="Post Author")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name="posts",
                              blank=True,
                              null=True,
                              verbose_name="Group",
                              help_text='This is the field for selecting the post group, '
                                        'it is optional.'
                              )
    image = models.ImageField(verbose_name='Image',
                              upload_to='posts/',
                              blank=True,
                              help_text='This field is for adding photos.')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]

class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Post Reference',
                             related_name='comments',
                             on_delete=models.CASCADE,
                             )
    author = models.ForeignKey(User, verbose_name='Author Reference',
                               related_name='comments',
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Comment Text')
    created = models.DateTimeField('Creation Date',
                                   auto_now_add=True,
                                   db_index=True)
    likes = models.ManyToManyField(User, verbose_name="Likes",
                                   related_name='users',
                                   blank=True
                                   )

    def get_likes(self):
        return self.likes.prefetch_related().count()

    def __str__(self):
        return f"{self.text}, likes: {self.likes}"

class Follow(models.Model):
    user = models.ForeignKey(User, verbose_name='Follower',
                             related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Following',
                               related_name='following',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'Follower: {self.user}, Following: {self.author}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique_follow')
        ]
