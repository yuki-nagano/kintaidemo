from unicodedata import name
from django.contrib import admin
from .models import Kintai

# Register your models here.
class KintaiAdmin(admin.ModelAdmin):
    model = Kintai
    list_display = ('u_id', 'workingday', 'begintime', 'finishtime', 'breaktime')
    search_fields = ('u_id',)

admin.site.register(Kintai, KintaiAdmin)