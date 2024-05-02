from django.shortcuts import render
from django.contrib.auth import views as base_views
from django.conf import settings

from . import forms

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode

session_string = '{app_name}-user={user}&{app_name}-pw={pw}'

# Generates a url-encoded session string based on username and session
def generate_httpd_session(username, session):
     return session_string.format(app_name=settings.APP_NAME, user=username, pw=session.session_key) # Session key is used as a password


# Create your views here.
class LoginView(base_views.LoginView):
    form_class = forms.LoginForm

    def form_valid(self, form):
        # Allow remember-me functionality
        
        # Based on https://stackoverflow.com/a/53431981
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is set 
            self.request.session.modified = True

        response = super().form_valid(form)
          
        # Set httpd session
        response['X-Replace-Session'] = generate_httpd_session(self.request.POST['username'], self.request.session)

        return response


class LogoutView(base_views.LogoutView):

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)

        return response


def get_httpd_session(request):
     next = request.GET.get('next','/')
     if request.user.is_authenticated:
          response = HttpResponseRedirect(next)
          response['X-Replace-Session'] = generate_httpd_session(request.user.username, request.session)
     else:
          next = "{}?{}".format(reverse('login'), urlencode({'next': next}))
          response = HttpResponseRedirect(next)
          
     return response


class PasswordResetView(base_views.PasswordResetView):
    form_class = forms.PasswordResetForm
