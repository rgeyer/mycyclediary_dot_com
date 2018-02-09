from django.conf.urls import include, url
import mycyclediary_dot_com.apps.www.views
from rest_framework.documentation import include_docs_urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^api/', include('mycyclediary_dot_com.apps.api.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^connect', mycyclediary_dot_com.apps.www.views.login, name='login'),
    # url(r'^logout', mycyclediary_dot_com.apps.www.views.logout),
    url(r'^api_docs', include_docs_urls(title='MyCycleDiary API Docs')),
    url(r'^.*$', mycyclediary_dot_com.apps.www.views.index, name='index'),
]
