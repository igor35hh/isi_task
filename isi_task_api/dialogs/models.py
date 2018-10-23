from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from dialogs.mixins import TimeStampedModel


class Thread(TimeStampedModel):
    
    participants = models.ManyToManyField(CustomUser, related_name='threads', 
                                          verbose_name=_("participants"))
    
    class Meta:
        verbose_name = _("thread")
        verbose_name_plural = _("threads")
        ordering = ('-created', )
        
    
class Message(TimeStampedModel):
    
    text   = models.TextField(verbose_name=_("message"), null=True, blank=True)
    sender = models.ForeignKey(CustomUser, verbose_name=_("user"), on_delete=models.PROTECT)
    thread = models.ForeignKey(Thread, verbose_name=_("thread"), 
                               related_name='messages', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ('-created', )    
