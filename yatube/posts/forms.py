from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Это поле для текста '
            'поста, оно не имеет ограничений '
            'на количество символов.',
            'group': 'Это поле выбора группы поста, '
            'оно необязательное.'
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            "text": forms.TextInput(attrs={"id": "chat-message-input"})}
