import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import UpdateView
from django.shortcuts import redirect

from kintaiapp.models import Kintai, WorkingStatus
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import csv

# ログ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATUS_FOR_DISPLAY = {
    True: "End working",
    False: "Start working"
}


###
#  HOME
#  - ホーム画面
###
def home(request):
    # テスト用（削除予定）
    record = WorkingStatus.objects.all()
    if len(record) == 0:
        WorkingStatus.objects.create(
            u_id=180,
            isworking=False
        )

    u_id = 180  # TODO とりあえず今は固定
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
    header = ['u_id', 'start time', 'end time', 'breaktime']
    writer.writerow(header)

    # export records of this month
    this_month = datetime.now().month
    data = Kintai.objects.filter(begintime__month=this_month)
    for i in data:
        writer.writerow([i.u_id, i.begintime, i.finishtime, i.breaktime])

    return response


###
#  DOKINTAI
#  - 勤怠入力機能
###
# 同じ日のレコードが2つ以上ある場合
# 出勤時間の場合退勤時間の場合どっちかに処理を寄せる
# 出勤時間が古い方を採用？
# 退勤時間が遅い時間を採用？
def dokintai(request):
    u_id = 180  # TODO とりあえず今は固定
    current_status = WorkingStatus.objects.get(u_id=u_id)

    logger.debug(f'Update Kintai - id={u_id} working status is {current_status.isworking}')

    # ステータスチェック
    if current_status.isworking:
        # 退勤時間記入
        # finishtimeがnullのレコードを取得 (同日関係なく)
        kintai_data = Kintai.objects.get(
            u_id=u_id,
            finishtime=None
        )
        if kintai_data:
            # 退勤打刻時に日付が当日以外の場合
            if kintai_data.workingday != datetime.today():
                # (1) 退勤時間を今日の0:00にする
                dt = datetime.now()
                midnight_time = dt.replace(hour=0, minute=0, second=0, )
                kintai_data.finishtime = midnight_time
                # (2) 出勤時間0:00, 退勤時間現時刻で新しいレコードを追加
                new_kintai_data = Kintai.objects.create(
                    u_id=u_id,
                    workingday=datetime.today(),
                    begintime=midnight_time,
                    finishtime=datetime.now(),
                )
                new_kintai_data.save()
            else:
                # 休憩時間計算
                endtime = datetime.now()
                breaktime = _calc_breaktime(kintai_data.begintime, endtime)
                # 更新
                kintai_data.finishtime = endtime
                kintai_data.breaktime = breaktime
        else:
            # isworkingでレコードがない場合：退勤時間のみを記入しレコード追加 TODO
            kintai_data = Kintai.objects.create(
                u_id=u_id,
                workingday=datetime.today(),
                finishtime=datetime.now(),

            )
        # isWorkingのフラグ下ろす
        current_status.isworking = False
    else:
        # 出勤時間記入 (勤怠レコード追加)
        kintai_data = Kintai.objects.create(
            u_id=u_id,
            workingday=datetime.today(),
            begintime=datetime.now(),
        )
        # isWorkingのフラグ上げる
        current_status.isworking = True

    # 更新内容を保存
    kintai_data.save()
    current_status.save()

    logger.debug(f'Successfully saved Kintai - id={u_id} working status is now {current_status.isworking}')

    res_dict = {
        'text': STATUS_FOR_DISPLAY[current_status.isworking]
    }

    return render(request, "kintaiapp/home.html", res_dict)


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
        return timedelta(seconds=1800)
    elif total_hour.seconds >= 28800:
        # 8時間以上
        return timedelta(seconds=3600)


###
# RECORD VIEWS
#  - 勤怠一覧表示
###
class RecordViews(View):

    def get(self, request):
        # Get values from query params
        if 'month' in request.GET and 'year' in request.GET:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
        else:
            # if there's no query params, show this month
            year = datetime.today().year
            month = datetime.today().month

        data_dict = self._get_record_by_month(year, month)
        return render(request, 'kintaiapp/record.html', data_dict)

    ###
    # Get record by month
    # 月毎の勤怠を取得
    # param:
    #   year : int
    #   month: int
    ###
    def _get_record_by_month(self, year: int, month: int) -> dict:
        date = datetime(year, month, 1)
        data = Kintai.objects.filter(begintime__year=year, begintime__month=month).order_by(
            'workingday')  # memo: order_by 降順は'-id'
        last_month = date - relativedelta(months=1)
        next_month = date + relativedelta(months=1)
        data_dict = {
            'kintailist': data,
            'datelist': [
                {
                    'lastmonth_year': last_month.year,
                    'lastmonth_month': last_month.month,
                    'nextmonth_year': next_month.year,
                    'nextmonth_month': next_month.month,
                }
            ],
        }

        return data_dict


###
# RECORD UPDATE VIEWS
#  - 勤怠編集
###
class RecordUpdateViews(UpdateView):
    template_name = 'kintaiapp/edit.html'
    model = Kintai
    fields = ('workingday', 'begintime', 'finishtime', 'breaktime')

    def form_valid(self, form):
        post = form.save()
        return redirect('record')
