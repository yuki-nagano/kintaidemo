from django.urls import path
from . import views
from .views import RecordViews

urlpatterns = [
    path('', views.home, name='home'),
    path('dokintai', views.dokintai, name='dokintai'),
    path('record', RecordViews.as_view(), name='record'),
    path('record/monthly', RecordViews.as_view(), name='record/monthly'),
    path('export/csv', views.export_csv, name='export_csv'),
]