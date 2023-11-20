from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import login, logout

from authorization.forms import NativeUserCreationForm, NativeAuthenticationForm
from authorization.infrastructure.enums import *
from authorization.static_text.static_text import *


def register(request):
    if request.method == 'POST':
        form = NativeUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, account_created_success_message)
            return redirect('vpnsite')

        else:
            messages.error(
                request, account_has_not_been_created__invalid_data__error_message
            )

    else:
        form = NativeUserCreationForm()

    return render(request, 'registration_window.html', context={'form': form, 'authorization_type': Authorization_type.REGISTRATION})

def authorize(request):
    if request.method == 'POST':
        form = NativeAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, log_in_success_message)
            return redirect('vpnsite')

        else:
            messages.error(request, log_in__invalid_data__error_message)

    else:
        form = NativeAuthenticationForm()
    return render(request, 'authorization_window.html', context={'form': form, 'authorization_type': Authorization_type.AUTHORIZATION})


def log_out(request):
    logout(request)
    return redirect('authorization')