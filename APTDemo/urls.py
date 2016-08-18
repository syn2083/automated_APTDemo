from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.demo_central, name='demo_central'),
]
