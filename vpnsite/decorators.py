import sys
from functools import wraps
from vpnsite.models import Statistics, Site, TrackedSite
from vpnsite.infrastructure.enums import StatisticsControlStatus

from sheepfish_vpn import urls

import re


def site_tracking(view):
    @wraps(view)
    def wrap(request, *args, **kwargs):
        user = request.user
        tracked_site, __ = TrackedSite.objects.get_or_create(user=user)
        try:  # site block
            site = Site.objects.get(url=kwargs['site_url'])
            tracked_site.site = site

        except Exception:  # resource block
            site = tracked_site.site

        tracked_site.save()

        return view(request, site, *args, **kwargs)

    return wrap


def statistics_control(view):

    @wraps(view)
    def wrap(request, site, *args, **kwargs):
        try:
            kwargs['site_url']
            status = StatisticsControlStatus.SiteControlling

        except Exception:
            status = StatisticsControlStatus.ResourceControlling

        statistics = Statistics.objects.get(site=site)
        match status:
            case StatisticsControlStatus.SiteControlling:
                statistics.transitions += 1
        statistics.volume += sys.getsizeof(request)

        response = view(request, site, *args, **kwargs)

        statistics.volume += sys.getsizeof(response)

        statistics.save()

        return response

    return wrap
