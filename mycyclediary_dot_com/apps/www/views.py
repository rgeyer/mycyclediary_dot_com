from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

@login_required
def index(request):
    return render(request, 'www/templates/index.html', {})

def login(request):
    return render(request, 'www/templates/login.html', {})

def logout(request):
    auth_logout(request)
    return redirect('/')
