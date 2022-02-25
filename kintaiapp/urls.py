from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('dokintai', views.dokintai),
    path('record', views.record, name='record'),
    # test
    path('hello', views.index),
]