from django.conf.urls import url
from Goodshow import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list(\d+)_(\d)_(\d)/$', views.goods_list),
    url(r'^(\d+)/$', views.goods_detail, name='detail'),

]
