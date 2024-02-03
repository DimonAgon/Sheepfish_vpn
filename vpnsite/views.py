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
from bs4.element import ResultSet

from typing import Type

import copy


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

def get_root_from_internal_url(url: str):
    root_url = re.match(urls.localhost_port_regex, url).group(0)
    return root_url

def recover_resource_relative_path_with_root(path: str, root_url):
    if re.match('\/', path) or not re.match(r'(http[s]{0,1})|(ftp[s]{0,1})(:\/\/)', path):     # resource path is relative

        recovered_resource_url = f"{root_url}/{path}"
        return recovered_resource_url

    else:
        return path

def substitute_resource_path(path: str):
    return f'{urls.on_vpn_site_visit_url}{path}'

class TextPathManipulator:
    def __init__(self, text):
        self.text: str = text
        self.manipulated_text: str = text
        self.souped: Type[BeautifulSoup] = BeautifulSoup(text, 'html.parser')
        self.manipulated_souped = copy.deepcopy(self.souped)
        self.tag_objects: ResultSet = self.souped.find_all()
        self.manipulated_tag_objects: ResultSet = self.manipulated_souped.find_all()
        self.is_manipulated: bool = False

    def manipulate_all_paths(self, path_manipulation_funtion, *args, **kwargs):
        if not self.is_manipulated:
            self.is_manipulated = True

        if self.manipulated_text:

            path_types = {'href', 'src'}
            for tag_object in self.manipulated_tag_objects:
                for path_type in path_types:
                    if tag_object.has_attr(path_type):
                        path = tag_object[path_type]
                        manipulated_path = path_manipulation_funtion(path, *args, **kwargs)
                        tag_object[path_type] = manipulated_path
                        break

            self.manipulated_tag_objects = self.manipulated_souped.find_all()
            self.manipulated_text = str(self.manipulated_souped)

@site_tracking
@statistics_control
def internal_resource(request, resource_url, site, *args, **kwargs):

    root_url = get_root_from_internal_url(resource_url)
    recovered_url = recover_resource_relative_path_with_root(resource_url, site)

    response = requests.request(method=request.method        ,
                                url=recovered_url            ,
                                params=request.content_params,
                                data=request.body            ,
                                headers=request.headers      ,
                                )
    http_response = convert_response_to_http_resp(response)

    text = response.text
    text_path_manipulator = TextPathManipulator(text)
    text_path_manipulator.manipulate_all_paths(recover_resource_relative_path_with_root, root_url=root_url)
    text_path_manipulator.manipulate_all_paths(substitute_resource_path)
    path_recovered_path_substitute_text = text_path_manipulator.manipulated_text
    path_recovered_path_substitute_response = http_response
    path_recovered_path_substitute_response.content = path_recovered_path_substitute_text

    return path_recovered_path_substitute_response


def external_site(request, site_url):
    return redirect(site_url)
