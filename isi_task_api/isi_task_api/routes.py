from rest_framework import routers
from dialogs.views import ThreadViewSet, MessageViewSet
from accounts.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'threads', ThreadViewSet, base_name='thread')
router.register(r'message', MessageViewSet, base_name='message')
router.register(r'users', CustomUserViewSet, base_name='customuser')
