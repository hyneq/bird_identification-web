from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UserCreationForm

# Based on https://stackoverflow.com/a/39660883
admin.site.unregister(User)

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'welcome'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        Form = super(UserAdmin, self).get_form(request, obj, **kwargs)

        if not obj:
            class FormWithRequest(Form):
                def __new__(cls, *args, **kwargs):
                    kwargs['request'] = request
                    return Form(*args, **kwargs)

            return FormWithRequest

        else:
            return Form

admin.site.register(User, UserAdmin)
