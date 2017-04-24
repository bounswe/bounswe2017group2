from django.conf.urls import url
from concert import views

urlpatterns = [
               url(r'^concert/$', views.concert_list),
               url(r'^concert/(?P<pk>[0-9]+)/$', views.concert_detail),
               ]
