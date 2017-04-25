from django.conf.urls import url
from concert import views


urlpatterns = [
               url(r'^admin/', admin.site.urls),
               
               url(r'^concert/$', views.concert_list),
               url(r'^concert/(?P<pk>[0-9]+)/$', views.concert_detail),
			   url(r'^user/$', views.user_list),
               url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail),
               ]


