import sys
from functools import wraps
from vpnsite.models import Statistics, Site, TrackedSite
from vpnsite.infrastructure.enums import StatisticsControlStatus

from sheepfish_vpn import urls

import re


def site_tracking(view):
    @wraps(view)
    def wrap(request, resource_url, *args, **kwargs):
        user = request.user
        tracked_site, __ = TrackedSite.objects.get_or_create(user=user)
        try:  # site block
            site = Site.objects.get(url=resource_url)
            tracked_site.site = site
                                 #TODO: undefined sites should not be considered as a resource of the tracked site
        except Exception:  # resource block
            site = tracked_site.site

        tracked_site.save()

        return view(request, resource_url, site, *args, **kwargs)

    return wrap


def statistics_control(view):

    @wraps(view)
    def wrap(request, resource_url, site, *args, **kwargs):
        try:
            Site.objects.get(url=resource_url)
            status = StatisticsControlStatus.SiteControlling

        except Exception:
            status = StatisticsControlStatus.ResourceControlling

        statistics = Statistics.objects.get(site=site)
        match status:
            case StatisticsControlStatus.SiteControlling:
                statistics.transitions += 1
        statistics.volume += sys.getsizeof(request)

        response = view(request, resource_url, site, *args, **kwargs)

        statistics.volume += sys.getsizeof(response)

        statistics.save()

        return response

    return wrap
