from django.urls import path

from . import views

urlpatterns = [
    path('api/upload', views.LoggedObjectUpload.as_view(), name='upload_objects')
]
