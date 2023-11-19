from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from vpnsite.models import Statistics, Site
from vpnsite.forms import AddSiteForm


def vpnsite(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        statistics, __ = Statistics.objects.get_or_create(user=user_object)
        sites = Site.objects.filter(user=user_object)
        context = {'user': user_object,
                   'statistics': statistics,
                   'sites': sites}
        return render(request, 'vpnsite.html', context=context)

    else:
        return redirect('authorization')


def add_site(request):
    if request.method == 'POST':
        user_object = User.objects.get(username=request.user)
        form = AddSiteForm(request.POST)
        if form.is_valid():
            new_site = Site.objects.create(**form.cleaned_data, user=user_object)
            new_site.save()
            return redirect('vpnsite')

    else:
        form = AddSiteForm()
        return render(request, 'add_site.html', context={'form': form})