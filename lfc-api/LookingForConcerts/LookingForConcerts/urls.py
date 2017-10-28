'''
LookingForConcerts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
'''
from django.conf.urls import url
from django.contrib import admin
from lfc_backend import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^concerts/$', views.list_concerts), # lists all concerts in DB
    url(r'^newconcert/$', views.create_concert), # creates a concert with provided info
    url(r'^concert/(?P<pk>[0-9]+)/$', views.concert_detail), # gets, modifies or deletes a specific concert
    url(r'^users/$',views.list_users), # lists all the users registered to our app
    url(r'^newuser/$',views.list_users), # creates a new user with provided info
    #url('^', include('django.contrib.auth.urls'))
    # auth.urls includes:
    # ^login/$ [name='login']
    # ^logout/$ [name='logout']
    # ^password_change/$ [name='password_change']
    # ^password_change/done/$ [name='password_change_done']
    # ^password_reset/$ [name='password_reset']
    # ^password_reset/done/$ [name='password_reset_done']
    # ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
    # ^reset/done/$ [name='password_reset_complete']
]
