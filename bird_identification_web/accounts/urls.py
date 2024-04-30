"""accounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views
from django.contrib.auth import views as django_views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_change/', django_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', django_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', django_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>', django_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete', django_views.PasswordResetCompleteView.as_view(template_name='registration/password_change_done.html'), name='password_reset_complete'),
]
