import sys
from functools import wraps
from vpnsite.models import Statistics, Site


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

