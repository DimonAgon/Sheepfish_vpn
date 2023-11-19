from django.db import models
from django.contrib.auth.models import User


class BaseUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Statistics(BaseUserData):
    transitions = models.IntegerField(verbose_name="site transitions", default=0)
    volume = models.FloatField(verbose_name="data volume", default=0)

class Site(BaseUserData):
    url = models.URLField(verbose_name="site url")
    name = models.CharField(verbose_name="site name", max_length=360)
