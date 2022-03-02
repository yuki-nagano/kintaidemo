import logging

from django.shortcuts import render
from django.http import HttpResponse

from kintaiapp.models import Kintai, WorkingStatus
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import csv

# ログ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


STATUS_FOR_DISPLAY = {
    True : "End working",
    False : "Start working"
}

###
#  HOME
#  - ホーム画面
###
def home(request):
    u_id = 180 # TODO とりあえず今は固定
    user = WorkingStatus.objects.get(u_id=u_id)
    # ステータスチェック
    res_dict = {
        'text': STATUS_FOR_DISPLAY[user.isworking]
        }
    return render(request, "kintaiapp/home.html", res_dict)

###
#  EXPORT as CSV
#  - CSVで出力
###
def export_csv(request):
    # ready a csv file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'

    writer = csv.writer(response)

    # Set the header
    header = ['u_id','start time','end time','breaktime']
    writer.writerow(header)

    # export records of this month
    this_month = datetime.now().month
    data = Kintai.objects.filter(begintime__month=this_month)
    for i in data:
        writer.writerow([i.u_id,i.begintime, i.finishtime,i.breaktime])

    return response

###
#  DOKINTAI
#  - 勤怠入力機能
###
def dokintai(request):
    u_id = 180 # TODO とりあえず今は固定
    current_status = WorkingStatus.objects.get(u_id=u_id)

    logger.debug(f'Update Kintai - id={u_id} working status is {current_status.isworking}')

    # ステータスチェック
    if current_status.isworking:
        # 退勤時間記入
        # 同日でfinishtimeがnullのレコードがあればupdateする
        kintai_today = Kintai.objects.get(
                            u_id=u_id, 
                            workingday=datetime.today(), 
                            finishtime=None
                            )
        if kintai_today:
            # 休憩時間計算
            endtime = datetime.now()
            breaktime = _calc_breaktime(kintai_today.begintime, endtime)
            # 更新
            kintai_today.finishtime = endtime
            kintai_today.breaktime = breaktime
        else:
            # isworkingでレコードがない場合：退勤時間のみを記入しレコード追加 TODO
            kintai_today = Kintai.objects.create(
            u_id=u_id,
            workingday=datetime.today(),
            finishtime=datetime.now(),
        )
        # isWorkingのフラグ下ろす
        current_status.isworking = False
    else:
        # 出勤時間記入 (勤怠レコード追加)
        kintai_today = Kintai.objects.create(
            u_id=u_id,
            workingday=datetime.today(),
            begintime=datetime.now(),
        )
        # isWorkingのフラグ上げる
        current_status.isworking = True

    # 更新内容を保存
    kintai_today.save()
    current_status.save()
    
    logger.debug(f'Successfully saved Kintai - id={u_id} working status is now {current_status.isworking}')

    res_dict = {
        'text': STATUS_FOR_DISPLAY[current_status.isworking]
        }
        
    return render(request, "kintaiapp/home.html", res_dict)


###
# RECORD
#  - 勤怠一覧表示
#  - 勤怠編集 (追加予定)
###
def record(request):
    # 一覧表示
    if request.method == 'GET':
        data = Kintai.objects.all().order_by('id') # memo: 降順は'-id'
        data_dict = {'kintailist': data}
        for i in data:
            if i.breaktime is None:
                i.breaktime = "-"
        return render(request, 'kintaiapp/record.html', data_dict)

###
# Calculate break time with start time and end time
# 開始時間と終了時間から休憩時間を計算
# 
# 現在の設定
# 　 - 4時間勤務：30分休憩
# 　 - 8時間勤務：1時間休憩
###
def _calc_breaktime(start, end):
    total_hour = end - start 
    if total_hour.seconds < 14400:
        # 4時間未満
        return timedelta()
    elif total_hour.seconds >= 14400 and total_hour < 28800:
        # 4時間以上8時間未満
        return datetime.timedelta(seconds = 1800)
    elif total_hour.seconds >= 28800:
        # 8時間以上
        return datetime.timedelta(seconds = 3600)

