# Create your views here.
from django.http import HttpResponse
import django

def index(request):
    return HttpResponse(django.VERSION)
