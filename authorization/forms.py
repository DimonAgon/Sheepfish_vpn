
from django.forms import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class NativeUserCreationForm(UserCreationForm):
    username = CharField(
        label="Username",
        widget=TextInput(
            attrs={'class': "field", 'autofocus': True}
        )
    )

    email = EmailField(
        label="Email",
        widget=TextInput(
            attrs={'type': "email", 'class': "field"}
        )
    )

    password1 = CharField(
        label="Password",
        widget=TextInput(
            attrs={'type': "password", 'class': "field"}
        )
    )

    password2 = CharField(
        label="Password re-enter",
        widget=TextInput(
            attrs={'type': "password", 'class': "field"}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NativeAuthenticationForm(AuthenticationForm):
    username = CharField(
        label="Username",
        widget=TextInput(
            attrs={'class': "field", 'autofocus': True}
        )
    )

    password = CharField(
        label="Password",
        widget=TextInput(
            attrs={'type': "password", 'class': "field"}
        )
    )