from django.urls import path

from . import views

urlpatterns = [
    path('', views.dokintai),
    # test
    path('hello', views.index),
]