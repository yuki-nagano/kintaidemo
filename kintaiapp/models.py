from django.db import models

# Create your models here.

class Kintai(models.Model):
    id = models.AutoField(primary_key=True)
    u_id = models.IntegerField(blank=False)
    workingday = models.DateField(blank=True, null=True )
    begintime = models.DateTimeField(blank=True, null=True)
    finishtime = models.DateTimeField(blank=True, null=True)
    breaktime = models.DurationField(blank=True, null=True)
    
    class Meta:
        db_table = 'kintai'

class WorkingStatus(models.Model):
    u_id = models.IntegerField(primary_key=True)
    isworking = models.BooleanField()

    class Meta:
        db_table = 'working_status'


class T_NYUUSYUKKOKEKKA(models.Model):
    id = models.AutoField(primary_key=True)
    itemNO = models.TextField(null=True)
    meisyou = models.TextField(null=True)
    HINMOKUType = models.TextField(null=True)
    TANABAN_N = models.TextField(null=True)
    SUURYOU = models.IntegerField()
    KAISUU = models.IntegerField()
    MEMO1 = models.TextField(null=True)
    MEMO2 = models.TextField(null=True)
    TANABINITIJI = models.DateTimeField(blank=True, null=True)
    TANAIREBIMIN = models.DateTimeField(blank=True, null=True)
    TANAOROSHINO = models.TextField(null=True)
    TANAOROSHIBI = models.DateTimeField(blank=True, null=True)
    TANAOROSHISAI = models.TextField(null=True)
    TANAOROSHIKAISUU = models.IntegerField()
    TANAOPrint = models.BooleanField()
    TANAOPrintBI = models.DateTimeField(blank=True, null=True)
    TANAOPrintSYA = models.TextField(null=True)
    TANAOPrintSYAmei = models.TextField(null=True)
    KUBUN = models.IntegerField(null=True)
    MRPKANRISYA = models.TextField(null=True)
    IDOUck = models.BooleanField()
    IDOUbi = models.DateTimeField(blank=True, null=True)
    IDOUsya = models.TextField(null=True)
    IDOUsaki = models.TextField(null=True)

    class Meta:
        db_table = 'T_NYUUSYUKKOKEKKA'