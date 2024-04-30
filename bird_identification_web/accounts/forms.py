from django.contrib.auth import forms as base_forms
from django.contrib.auth.models import User
from django import forms as django_forms
from django.utils.translation import gettext_lazy as _
from accounts.email import send_welcome_email

class LoginForm(base_forms.AuthenticationForm):
    # Based on https://stackoverflow.com/a/53981051
    username = base_forms.UsernameField(
        label=_('Username or email'), # Set a label that indicates an email address can be used
        widget=django_forms.TextInput(attrs={'autofocus': True})
    )

    # Based on https://stackoverflow.com/a/53431981
    remember_me = django_forms.BooleanField(label=_('Remember me'), required=False)  # add the remember_me field

class PasswordResetForm(base_forms.PasswordResetForm):
    def get_users(self, email):
        """Based on the original get_users().
        Allows users with unusable passwords to reset their password
        """
        email_field_name = base_forms.UserModel.get_email_field_name()
        active_users = base_forms.UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if base_forms._unicode_ci_compare(email, getattr(u, email_field_name))
        )

# Based on https://stackoverflow.com/a/5745488
class UserCreationForm(django_forms.ModelForm):
    username = django_forms.CharField(label = _("Username"))
    email = django_forms.EmailField(label = _("Email"))
    welcome = django_forms.BooleanField(label = _("Send welcome message"), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "welcome")

    # Based on https://stackoverflow.com/a/9191583
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # access request from any method as self.request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.set_unusable_password()

        user.save()

        if self.cleaned_data["welcome"]:
            send_welcome_email(user=user, request=self.request)

        return user
