from django.urls import path

from . import views

urlpatterns = [
    path('api/upload', views.LoggedObjectUpload.as_view(), name='upload_objects'),

    path('<str:timespan_name>/<str:time_input>', views.index, name='object_statistics'),
    path('', views.index, name='object_statistics_default'),
    path('<str:timespan_name>/', views.index)
]
