from django.contrib import admin

from vpnsite.models import Site, Statistics, TrackedSite

for model in Site, Statistics, TrackedSite:
    admin.site.register(model)
