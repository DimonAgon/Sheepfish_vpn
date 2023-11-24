"""
URL configuration for sheepfish_vpn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from vpnsite.views import vpnsite, add_site, internal_site, external_site
from authorization.views import register, authorize, log_out

import re

localhost_port_regex = re.compile('(((http[s]{0,1})|(ftp[s]{0,1}))(:\/\/)){0,1}'
                             '(?:(?:(localhost)|(127\.0\.0.1)|((?:0\.){3}0))):'
                             '(65535|6553[0-4]|655[0-2]\d|65[0-4]\d{1,2}|6[0-4]\d{1,3}|[0-5]\d{1,4}|\d{1,4})')

ending_regex = re.compile('\/{0,1}')

internal_site_url_regex = r'^vpnsite\/site\/{}\/.+{}$'.format(localhost_port_regex.pattern, ending_regex.pattern)

on_vpn_site_visit_url = 'vpnsite/site/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vpnsite/', vpnsite, name='vpnsite'),
    re_path(internal_site_url_regex, internal_site),
    path('vpnsite/site/<path:site_url>', external_site),
    path('addsite', add_site, name='addsite'),
    path('registration/', register, name='registration'),
    path('authorization', authorize, name='authorization'),
    path('logout', log_out, name='logout'),
]
