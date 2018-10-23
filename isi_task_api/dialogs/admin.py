from django.contrib import admin
from accounts.models import USERTYPE_ADMIN
from dialogs.models import Thread, Message
from dialogs.forms import ThreadEditForm


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('created', 'updated')
    list_filter = ('created',)
    readonly_fields = ('created', 'updated')

    form = ThreadEditForm
    model = Thread

    def has_delete_permission(self, request, obj=None):
        perm = admin.ModelAdmin.has_delete_permission(self, request, obj=obj)
        if request.user.user_type != USERTYPE_ADMIN:
            perm = False
        return perm

    def has_add_permission(self, request):
        perm = admin.ModelAdmin.has_add_permission(self, request)
        if request.user.user_type != USERTYPE_ADMIN:
            perm = False
        return perm


admin.site.register(Thread, ThreadAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'sender', 'thread')
    list_filter = ('created',)
    search_fields = ('text', 'sender', 'thread')
    readonly_fields = ('created', 'updated')


admin.site.register(Message, MessageAdmin)
