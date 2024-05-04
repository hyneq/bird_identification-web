"""bird_identification_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from django.views.generic.base import TemplateView

from django.conf import settings

import stream.views


urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('stream/', stream.views.index, name='stream'),
    path(settings.STREAM_INTERFACE_PATH.lstrip("/")+"/index.m3u8", stream.views.stream, name='stream_interface'),
    path('statistics/', include('object_statistics.urls')),
    path('empty/', TemplateView.as_view(template_name="base.html")),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]
