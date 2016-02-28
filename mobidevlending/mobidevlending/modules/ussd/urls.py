__author__ = 'Lawrence'

from django.conf.urls import url

from mobidevlending.modules.ussd.views import views
from mobidevlending.modules.ussd.views import dynamic_ussd

app_name = 'ussd'

urlpatterns = [
    url(r'^ussd', views.ussd, name='ussd'),
    url(r'^dynamic_ussd', dynamic_ussd.ussd, name='dynamic_ussd'),
]