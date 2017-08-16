from django.conf.urls import patterns, include, url
from mycyclediary_dot_com.apps.strava import views

urlpatterns = [
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^bikes$', views.bikes, name='bikes'),
    url(r'^components$', views.components, name='components'),
    url(r'^bike_stats$', views.bike_stats, name='bike_stats'),
]
