from functools import wraps

from django.shortcuts import redirect

from django.contrib import messages
from authorization.static_text.static_text import *


def redirect_unauthorized_users(user_function):
    @wraps(user_function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return user_function(request, *args, **kwargs)

        else:
            messages.error(request, authorization_suggestion_error_message)
            return redirect('authorization')
    return wrap