# Based on https://stackoverflow.com/a/53431981

from django.shortcuts import render
from django.contrib.auth import views as base_views

from . import forms

# Create your views here.
class LoginView(base_views.LoginView):
    form_class = forms.LoginForm

    def form_valid(self, form):
        # Allow remember-me functionality
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is set 
            self.request.session.modified = True

        return super().form_valid(form)


class LogoutView(base_views.LogoutView):

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)

        return response


class PasswordResetView(base_views.PasswordResetView):
    form_class = forms.PasswordResetForm
