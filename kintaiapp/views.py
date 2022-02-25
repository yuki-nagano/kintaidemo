from datetime import date, datetime
from xmlrpc.client import Boolean
from django.shortcuts import render
from django.http import HttpResponse

from kintaiapp.models import Kintai, WorkingStatus
from django.utils.timezone import localtime
from django.utils import timezone

# List all endpoints


status_for_display = {
    0: "End working",
    1: "Start working"
}

def index(request):
    # Hello world for testing 
    return HttpResponse('Hello World')

def home(request):
    data = WorkingStatus.objects.filter(u_id=180) # とりあえずidは固定
    for user in data:
        # ステータスチェック
        res_dict = {
            'text': _get_display_stat(user.isworking)
            }
    return render(request, "kintaiapp/home.html", res_dict)

def dokintai(request):
    return render(request, "kintaiapp/home.html")

"""
    RECORD
    - 勤怠一覧表示
    - 勤怠編集 (追加予定)
"""
def record(request):
    # 一覧表示
    if request.method == 'GET':
        data = Kintai.objects.all()
        data_dict = {'kintailist': data}
        for i in data:
            if i.breaktime is None:
                i.breaktime = "-"
        return render(request, 'kintaiapp/record.html', data_dict)
    
"""
    Return status depending on isWorking
    isWorkingのステータスによって Start working か End working を返す
"""
def _get_display_stat(isWorking: bool) -> str:
    status = status_for_display[0] if isWorking else status_for_display[1]
    return status
