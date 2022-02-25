from django.db import models

# Create your models here.

class Kintai(models.Model):
    id = models.IntegerField(primary_key=True)
    u_id = models.IntegerField()
    workingday = models.DateField(blank=True, null=True )
    begintime = models.DateTimeField(blank=True, null=True)
    finishtime = models.DateTimeField(blank=True, null=True)
    breaktime = models.DurationField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'kintai'

class WorkingStatus(models.Model):
    u_id = models.IntegerField(primary_key=True)
    isworking = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'working_status'

