from django.contrib import admin

from vpnsite.models import Site, Statistics, ControlledSite

for model in Site, Statistics, ControlledSite:
    admin.site.register(model)
