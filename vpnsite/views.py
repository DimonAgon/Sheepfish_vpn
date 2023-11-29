from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from vpnsite.models import Statistics, Site
from vpnsite.forms import AddSiteForm
from authorization.decorators import redirect_unauthorized_users
from vpnsite.decorators import statistics_control, site_tracking

import requests
from django.http import HttpResponse
from sheepfish_vpn import urls

import re

from bs4 import BeautifulSoup


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


def convert_response_to_http_resp(response):
    http_response = HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )

    return http_response


def recover_resource_relative_path_with_root(site, resource_url):
    if re.match('\/', resource_url) or not re.match(r'(http[s]{0,1})|(ftp[s]{0,1})(:\/\/)', resource_url):     # resource path is relative

        root_url = ''.join(re.findall(urls.localhost_port_regex, site.url)[-1])
        recovered_resource_url = f"{root_url}/{resource_url}"
        return recovered_resource_url

    else:
        return resource_url

def swap_external_css_to_internal(text, site):
    if text:
        internal_css_text = text
        souped = BeautifulSoup(text, 'html.parser')
        css = souped.find_all('link', rel="stylesheet")
        for tag_object in css:
            href = tag_object['href']
            resource_fullpath = recover_resource_relative_path_with_root(site, href)
            css_unit_response = requests.get(resource_fullpath)
            css_unit_text = css_unit_response.text
            try:
                to_swap = re.search(r'<link.*href=[\'\"]{}[\'\"].*>'.format(href), internal_css_text).group(0)
                internal_css_text = internal_css_text.replace(to_swap, f'<style>{css_unit_text}</style>')

            except Exception:
                continue

        return internal_css_text

    else:
        return text

@site_tracking
@statistics_control
def internal_site(request, site, *args, **kwargs):
    site_url = kwargs['site_url']
    response = requests.get(site_url)
    http_resp = convert_response_to_http_resp(response)

    text = response.text
    inline_css_text = swap_external_css_to_internal(text, site)
    inline_css_http_resp = http_resp
    inline_css_http_resp.content = inline_css_text

    return inline_css_http_resp


@site_tracking
@statistics_control
def external_resource(request, site, *args, **kwargs):
    resource_url = kwargs['resource_url']

    recovered_url = recover_resource_relative_path_with_root(site, resource_url)

    response = requests.request(method=request.method  ,
                                url=recovered_url      ,
                                params=request.GET     ,
                                data=request.POST      ,
                                headers=request.headers,
                                )

    http_response = convert_response_to_http_resp(response)

    text = response.text
    inline_css_text = swap_external_css_to_internal(text, site)
    inline_css_http_resp = http_response
    inline_css_http_resp.content = inline_css_text

    substitute_response = inline_css_http_resp
    substitute_response.url = f"{urls.on_vpn_site_visit_url}{resource_url}"

    return substitute_response


def external_site(request, site_url):
    return redirect(site_url)