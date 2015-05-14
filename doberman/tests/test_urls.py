from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login

from doberman.decorators import watch_login

urlpatterns = patterns('',
                       url(r'^login/$', watch_login(login), name='login', kwargs={'template_name': 'login.html'}),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
                       )