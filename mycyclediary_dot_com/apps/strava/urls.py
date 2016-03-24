from django.conf.urls import patterns, include, url
from mycyclediary_dot_com.apps.strava import views

urlpatterns = [
    # Examples:
    url(r'^$', views.index, name='index'),
]
