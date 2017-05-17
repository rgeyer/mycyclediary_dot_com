from django.conf.urls import patterns, include, url
from mycyclediary_dot_com.apps.api import views

urlpatterns = [
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^strava/webhook/?$', views.strava_webhook_callback, name='strava_webhook_callback'),
]
