# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from .views import LoginUserView

urlpatterns = patterns(
    'accounts.views',
    # User authentication
    url(r'^login/$', LoginUserView.as_view(), name='login'),
    url(
        r'^logout/$',
        logout,
        {'template_name': 'accounts/logout.html'},
        name='logout'
    ),

)
