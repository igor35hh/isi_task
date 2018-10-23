from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("time created"))
    updated = models.DateTimeField(
        auto_now=True, verbose_name=_("time modified"))

    class Meta:
        abstract = True
