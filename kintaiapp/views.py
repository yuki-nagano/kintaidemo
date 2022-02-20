from django.shortcuts import render
from django.http import HttpResponse

# List all endpoints

def index(request):
    # Hello world for testing 
    return HttpResponse('Hello World')

def dokintai(request):
    return render(request, "kintaiapp/home.html")