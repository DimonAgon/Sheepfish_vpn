import sys
from functools import wraps
from vpnsite.models import Statistics, Site, ControlledSite
from vpnsite.infrastructure.enums import StatisticsControlStatus


def statistics_control(view):

    @wraps(view)
    def wrap(request, *args, **kwargs):
        user = request.user
        controlled_site, __ = ControlledSite.objects.get_or_create(user=user)

        try: #site block
            status = StatisticsControlStatus.SiteControlling

            site = Site.objects.get(url=kwargs['site_url'])
            controlled_site.site = site

        except Exception: #resource block
            status = StatisticsControlStatus.ResourceControlling

            site = controlled_site.site

        controlled_site.save()

        statistics = Statistics.objects.get(site=site)
        match status:
            case StatisticsControlStatus.SiteControlling:
                statistics.transitions += 1
        statistics.volume += sys.getsizeof(request)

        response = view(request, *args, **kwargs)

        statistics.volume += sys.getsizeof(response)

        statistics.save()

        return response

    return wrap

