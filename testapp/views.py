from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, World!")

def render_(request):
    return render(request, 'index.html')