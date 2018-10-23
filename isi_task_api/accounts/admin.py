from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + ((None, {
        'fields': ('user_type', )
    }),)

    add_fieldsets = DjangoUserAdmin.add_fieldsets + ((None, {
        'fields': ('user_type', )
    }),)

    list_display = DjangoUserAdmin.list_display + ('user_type', )


admin.site.register(User, UserAdmin)
