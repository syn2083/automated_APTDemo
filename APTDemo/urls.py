from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.demo_central, name='demo_central'),
    url(r'^demo/config/$', views.demo_config, name='demo_config'),
    url(r'^demo/controller/$', views.demo_controls, name='demo_controls'),
    url(r'^jif/config/$', views.jif_config, name='jif_config'),
    url(r'^automate/job_accepted/$', views.job_accepted, name='job_accepted'),
    url(r'^automate/reprint_sent/$', views.reprint_sent, name='reprint_sent'),
    url(r'^automate/proc_phase/$', views.proc_phase, name='proc_phase'),
    url(r'^automate/job_complete/$', views.job_complete, name='job_complete'),
    url(r'^start_demo/$', views.start_demo, name='start_demo'),
    url(r'^stop_demo/$', views.stop_demo, name='stop_demo'),
]
