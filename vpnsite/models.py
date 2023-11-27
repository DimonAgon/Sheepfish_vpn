from django.db import models
from django.contrib.auth.models import User


class BaseUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Site(BaseUserData):
    url = models.CharField(verbose_name="site url", max_length=2048) #TODO: change to URLfield, configure localhost url checking
    name = models.CharField(verbose_name="site name", max_length=360)


class Statistics(BaseUserData):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    transitions = models.IntegerField(verbose_name="site transitions", default=0)
    volume = models.FloatField(verbose_name="data volume", default=0)


class TrackedSite(BaseUserData):
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.SET_NULL)