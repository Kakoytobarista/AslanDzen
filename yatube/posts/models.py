from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name="Имя")
    slug = models.SlugField(unique=True,
                            verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title


class Post(CreatedModel):
    text = models.TextField(verbose_name="Текст поста",
                            help_text='Это поле для текста '
                                      'поста, оно не имеет ограничений '
                                      'на количество символов.', )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts",
                               verbose_name="Автор поста",
                               )
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name="posts",
                              blank=True,
                              null=True,
                              verbose_name="Группа",
                              help_text='Это поле выбора группы поста, '
                                        'оно необязательное.'
                              )
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='posts/',
                              blank=True,
                              help_text='Это поле для добавления'
                                        'фотографий')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Ссылка на пост',
                             related_name='comments',
                             on_delete=models.CASCADE,
                             )
    author = models.ForeignKey(User, verbose_name='Ссылка на автора',
                               related_name='comments',
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField('Дата создания',
                                   auto_now_add=True,
                                   db_index=True)
    likes = models.ManyToManyField(User, verbose_name="Лайки",
                                   related_name='users',
                                   blank=True
                                   )

    def get_likes(self):
        return len(self.likes.prefetch_related())

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
