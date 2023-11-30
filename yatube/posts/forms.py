from django import forms

from enums import PostModelEnum
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (PostModelEnum.TEXT.value, PostModelEnum.GROUP.value, PostModelEnum.IMAGE.value)
        help_texts = {
            'text': 'This field is for the text of the post, '
                    'it has no character limits.',
            'group': 'This is the field for selecting the post group, '
                     'it is optional.'
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (PostModelEnum.TEXT.value,)
        widgets = {
            "text": forms.TextInput(attrs={"id": "chat-message-input"})
        }
