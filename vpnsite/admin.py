from django.contrib import admin

from vpnsite.models import Site, Statistics

for model in Site, Statistics:
    admin.site.register(model)
