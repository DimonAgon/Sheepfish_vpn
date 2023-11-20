from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from vpnsite.models import Statistics, Site
from vpnsite.forms import AddSiteForm
from authorization.decorators import redirect_unauthorized_users

import requests
from django.http import HttpResponse


@redirect_unauthorized_users
def vpnsite(request):
    user_object = User.objects.get(username=request.user)
    statistics = Statistics.objects.filter(user=user_object)
    context = {'user': user_object,
               'statistics': statistics}
    return render(request, 'vpnsite.html', context=context)


@redirect_unauthorized_users
def add_site(request):
    if request.method == 'POST':
        user_object = User.objects.get(username=request.user)
        form = AddSiteForm(request.POST)
        if form.is_valid():
            new_site = Site.objects.create(**form.cleaned_data, user=user_object)
            new_site.save()
            Statistics.objects.create(user=user_object, site=new_site)
            return redirect('vpnsite')

    else:
        form = AddSiteForm()
        return render(request, 'add_site.html', context={'form': form})

def site(request, site_url):
    response = requests.get(site_url)

    http_response = HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )

    return http_response

def external_site(request, site_url):
    return redirect(site_url)