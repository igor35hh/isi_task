from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from dialogs.models import Thread
from accounts.models import USERTYPE_ADMIN
from sys import stdout


@receiver(m2m_changed, sender=Thread.participants.through)
def participants_changed(sender, instance, action, **kwards):
    if action in ['post_add', 'post_remove']:
        members = instance.participants.count()
        if members == 1:
            if instance.participants.all()[0].user_type == USERTYPE_ADMIN:
                try:
                    instance.delete()
                except TypeError as e:
                    stdout.write(str(e))
