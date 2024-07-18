from unicodedata import name
from django.contrib import admin
from .models import Kintai, T_NYUUSYUKKOKEKKA


# Register your models here.
class KintaiAdmin(admin.ModelAdmin):
    model = Kintai
    list_display = ('u_id', 'workingday', 'begintime', 'finishtime', 'breaktime')
    search_fields = ('u_id',)

# temp
# admin.site.register(Kintai, KintaiAdmin)

class InventoryAdmin(admin.ModelAdmin):
    model = T_NYUUSYUKKOKEKKA
    list_display = (
    "itemNO",
    "meisyou",
    "HINMOKUType",
    "TANABAN_N",
    "SUURYOU",
    "KAISUU",
    "MEMO1",
    "MEMO2",
    "TANABINITIJI",
    "TANAIREBIMIN",
    "TANAOROSHINO",
    "TANAOROSHIBI",
    "TANAOROSHISAI",
    "TANAOROSHIKAISUU",
    "TANAOPrint",
    "TANAOPrintBI",
    "TANAOPrintSYA",
    "TANAOPrintSYAmei",
    "KUBUN",
    "MRPKANRISYA",
    "IDOUck",
    "IDOUbi",
    "IDOUsya",
    "IDOUsaki",
    )
    search_fields = ('itemNO',)


admin.site.register(T_NYUUSYUKKOKEKKA, InventoryAdmin)
