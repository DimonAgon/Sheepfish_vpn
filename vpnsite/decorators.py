import sys
from functools import wraps
from vpnsite.models import Statistics, Site

def statistics_control(view):

    @wraps(view)
    def wrap(request, *args, **kwargs):
        path = request.path

        statistics = Statistics.objects.get(site=Site.objects.get(url=path))
        statistics.transitions += 1
        statistics.volume += sys.getsizeof(request)

        response = view(request, *args, **kwargs)

        statistics.volume += sys.getsizeof(response)

        statistics.save()

        return response

    return wrap
