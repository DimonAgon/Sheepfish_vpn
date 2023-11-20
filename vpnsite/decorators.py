import sys
from functools import wraps
from vpnsite.models import Statistics, Site

from sheepfish_vpn import urls


def pass_pure_site_url(view):

    @wraps(view)
    def wrap(request, *args, **kwargs):
        path = request.path
        site_url = path.replace(urls.on_vpn_site_visit_url, "", 1).replace("/", "", 1)

        return view(request, site_url, *args, **kwargs)

    return wrap


def statistics_control(view):

    @wraps(view)
    def wrap(request, site_url, *args, **kwargs):
        site = Site.objects.get(url=site_url)
        statistics = Statistics.objects.get(site=site)
        statistics.transitions += 1
        statistics.volume += sys.getsizeof(request)

        response = view(request, site_url)

        statistics.volume += sys.getsizeof(response)

        statistics.save()

        return response

    return wrap

