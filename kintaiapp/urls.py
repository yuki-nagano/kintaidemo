from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('dokintai', views.dokintai, name='dokintai'),
    path('record', views.record, name='record'),
]