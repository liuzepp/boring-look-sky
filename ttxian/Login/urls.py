from django.conf.urls import url
from Login.views import *

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^user_check/$', user_check),
    url(r'^register_check/$', register_check, name='zcyz'),
    url(r'^login/$', login, name='login'),
    url(r'^login_check/$', login_check, name='dlyz'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^info/$', info, name='info'),

    url(r'^user_order/$', user_order, name='uorder'),
    url(r'^site/$', user_site, name='site'),
    url(r'^save/$', user_save, name='save'),
]
