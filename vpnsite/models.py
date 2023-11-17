from django.db import models
from django.contrib.auth.models import User


class Statistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transitions = models.IntegerField(verbose_name="site transitions", default=0)
    volume = models.FloatField(verbose_name="data volume", default=0)
