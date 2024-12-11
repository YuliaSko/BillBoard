from allauth.account.forms import SignupForm
from django import forms
from board.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
import logging

from users.extensions import create_code
from ad_board import settings

logger = logging.getLogger(__name__)

# class BaseRegisterForm(UserCreationForm):
#     user_email = forms.EmailField(label='Email')
#     first_name = forms.CharField(label='Имя')
#     second_name = forms.CharField(label='Фамилия')
#
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'first_name',
#             'second_name',
#             'email',
#             'password1',
#             'password2',
#         )


class CommonSignupForm(SignupForm):
    # user_email = forms.EmailField(label='Email')
    # username = forms.CharField(label='Имя пользователя')
    first_name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Фамилия')

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = create_code()
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации аккаунта',
            message=f'Код активации: {user.code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return user
