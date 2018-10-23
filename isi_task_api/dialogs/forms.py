from django import forms
from accounts.models import USERTYPE_ADMIN
from dialogs.models import Thread
from django.utils.translation import gettext_lazy as _


class ThreadEditForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ('participants', )

    def clean_participants(self):
        participants = self.cleaned_data['participants']
        admins = participants.filter(user_type=USERTYPE_ADMIN).count()
        if admins > 1:
            raise forms.ValidationError(
                _('The field participants contains more than one admin.'))
        else:
            return self.cleaned_data['participants']
