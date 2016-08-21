from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.demo_central, name='demo_central'),
    url(r'^demo/config/$', views.demo_config, name='demo_config'),
    url(r'^jif/config/$', views.jif_config, name='jif_config'),
    url(r'^automate/job_accepted/$', views.job_accepted, name='job_accepted'),
    url(r'^home/$', views.current_times, name='current_times'),
]
