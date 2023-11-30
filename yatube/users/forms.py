from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from enums import UserModelEnum

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (UserModelEnum.FIRST_NAME.value, UserModelEnum.LAST_NAME.value,
                  UserModelEnum.USERNAME.value, UserModelEnum.EMAIL.value)
