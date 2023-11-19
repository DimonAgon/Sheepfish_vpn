from functools import wraps

from django.shortcuts import redirect


def redirect_unauthorized_users(user_function):
    @wraps(user_function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return user_function(request, *args, **kwargs)

        else:
            return redirect('authorization')
    return wrap