from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

def index(request):
    return render(request, 'angular/index.html', {})
