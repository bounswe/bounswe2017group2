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
from rest_framework.authtoken import views as tokenviews #for acquiring token for a user
from lfc_backend import views
from django.conf.urls import include

from django.views import generic
from rest_framework.schemas import get_schema_view

from LookingForConcerts import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    # JWT AUTHENTICATION
    #url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),

    url(r'^$', generic.RedirectView.as_view(
         url='/api/', permanent=False)),
    url(r'^api/$', get_schema_view()),
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^api/auth/token/verify/$', TokenVerifyView.as_view()),
    #url(r'^accounts/', include('allauth.urls')),

    # USER
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^delete_user/(?P<pk>[0-9]+)/$', views.delete_user, name='delete_user'),
    url(r'^delete_all_users/$', views.delete_all_users, name='delete_all_users'),
    url(r'^login/$', views.registered_user_login, name='registered_user_login'),
    url(r'^logout/$', views.registered_user_logout, name='registered_user_logout'),
    url(r'^users/$',views.list_users), # lists all the users registered to our app
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^logged_in_user/$', views.get_logged_in_user),
    # CONCERT
    url(r'^concert/(?P<pk>[0-9]+)/subscribe/$', views.subscribe_concert), #subscribes logged in user to concert
    url(r'^concert/(?P<pk>[0-9]+)/unsubscribe/$', views.unsubscribe_concert), #unsubscribes logged in user from concert
    url(r'^concerts/$', views.list_concerts), # lists all concerts in DB
    url(r'^newconcert/$', views.create_concert), # creates a concert with provided info
    url(r'^concert/(?P<pk>[0-9]+)/$', views.concert_detail), # gets, modifies or deletes a specific concert
    #ARTIST
    url(r'^searchartists/', views.search_artists), #searches given artist string in spotify artists. Connects to spotify
    # COMMENT
    url(r'^concert/(?P<pk>[0-9]+)/newcomment/$', views.create_comment), #adds new comment to the concert specified by its primary key
    # RATING
    url(r'^concert/(?P<pk>[0-9]+)/rate/$', views.rate_concert),
    # LOCATION
    url(r'^locations/$',views.list_locations), # lists all locations in DB
    url(r'^location/(?P<pk>[0-9]+)/$',views.location_detail), # gets a specific location in DB
    # TAG
    # REPORT
    # RATING
    #TOKEN
    url(r'^get_token/$', views.get_token) #Returns users token given the email and password of the user
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

if settings.ADMIN_ENABLED:
    urlpatterns.append(
        url(r'^admin/', include(admin.site.urls)),
        # ..maybe other stuff you want to be dev-only, etc...
        )
