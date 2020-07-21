from django.conf.urls import url
from Char import views

urlpatterns = [
    url(r'^cart/$', views.char),
    url(r'^removechar/$', views.removechar),
    url(r'^addchar/$', views.add_char),
    url(r'^edit/$', views.edit),
]
