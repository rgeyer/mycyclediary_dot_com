from django.conf.urls import include, url
from mycyclediary_dot_com.apps.api import views
from rest_framework_nested import routers
from mycyclediary_dot_com.apps.api.views import AthleteViewSet, ComponentViewSet, ActivityViewSet, LoginView, LogoutView, StravaViewSet

router = routers.SimpleRouter()
router.register(r'athletes', AthleteViewSet)
router.register(r'components', ComponentViewSet)
router.register(r'activities', ActivityViewSet, base_name='activity')
router.register(r'strava', StravaViewSet, base_name='strava')

urlpatterns = [
    # Examples:
    #url(r'^$', views.index, name='index'),
    #url(r'^strava/webhook/?$', views.strava_webhook_callback, name='strava_webhook_callback'),
    url(r'', include(router.urls)),
    url(r'^auth/login/$', LoginView.as_view(), name='login'),
    url(r'^auth/logout/$', LogoutView.as_view(), name='logout'),
]
