from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from vpnsite.models import Statistics


def vpnsite(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        statistics, __ = Statistics.objects.get_or_create(user=user_object)
        context = {'user': user_object,
                   'statistics': statistics}
        return render(request, 'vpnsite.html', context=context)

    else:
        return redirect('authorization')
