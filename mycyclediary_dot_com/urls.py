from django.conf.urls import patterns, include, url
import mycyclediary_dot_com.apps.www.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^$', mycyclediary_dot_com.apps.www.views.index, name='index'),
    url(r'^strava/', include('mycyclediary_dot_com.apps.strava.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^connect', mycyclediary_dot_com.apps.www.views.login, name='login'),
    url(r'^logout', mycyclediary_dot_com.apps.www.views.logout),
]
