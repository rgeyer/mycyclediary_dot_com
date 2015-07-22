from django.conf.urls import patterns, include, url
from mycyclediary_dot_com.apps.strava import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^request_auth', views.request_auth, name='request_auth'),
    url(r'^authorize', views.authorize, name='authorize')
)
