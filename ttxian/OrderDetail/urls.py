from django.conf.urls import url
from OrderDetail.views import *

urlpatterns = [
    url(r'^addorder/$', addorder, name='order'),
    url(r'^do_order/$', do_order),
    url(r'^check_pay/$', check_pay),

]
