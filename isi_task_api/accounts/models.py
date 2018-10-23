from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timedelta
from isi_task_api import settings
from rest_framework.authtoken.models import Token

USERTYPE_ADMIN = 'admin'
USERTYPE_DEFAULT = 'driver'

class CustomUser(AbstractUser):
    
    users_types = (('admin', 'Admin'), ('driver', 'Driver'),)
    user_type = models.CharField(max_length=25, choices=users_types, 
                                 verbose_name=_('user type'), default='driver')
    
    USERTYPE_FIELD = 'user_type'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key 
        

    