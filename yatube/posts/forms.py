from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Это поле для текста '
            'поста, оно не имеет ограничений '
            'на количество символов.',
            'group': 'Это поле выбора группы поста, '
            'оно необязательное.'
        }
