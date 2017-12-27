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
from django.conf.urls import include
from django.conf.urls.static import static

from django.views import generic
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view # for API Documentation with Swagger

from LookingForConcerts import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.contrib.auth.views import logout # for user logout

#API_PREFIX = r'^v(?P<version>[0-9]+\.[0-9]+)'

urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(
         url='/api/', permanent=False)), # redirect to /api/ if no matches are found
    url(r'^api/$', get_swagger_view(title='Looking for Concerts API')), # our API Documentation
    # for drf Open API - if we want to switch to it later
    #url(f'{API_PREFIX}/schema/', views.MySchemaView.as_view(title='Looking For Concerts API'), name='api_schema'),

    # JWT AUTHENTICATION
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()), # obtains a new JWT Access Token
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()), # refreshes the JWT Access Token
    url(r'^api/auth/token/verify/$', TokenVerifyView.as_view()), # verifies a JWT Access Token
    # USER
    url(r'^signup/$', views.signup, name='signup'), # registers a new user

    url(r'^login/$', TokenObtainPairView.as_view()), # logs the user in
    url(r'^logout/$', logout, name='logout'), # logs the user out
    url(r'^users/$',views.list_users), # lists all the users registered to our app
    # USER SEARCH
    url(r'^users/search/$',views.search_users), # returns a list of users if their username, first_name, last_name or spotify_display_name contains the search query.

    url(r'^user/me/$', views.get_user_info), # returns the logged in user object; requires authorization
    url(r'^user/edit_profile/$', views.edit_profile), # updates the information of the user
    url(r'^user/(?P<reported_user_id>[0-9]+)/report/$', views.create_or_edit_user_report), # creates or edits a user report for the user with the given pk
    url(r'^userreport/(?P<user_report_id>[0-9]+)/delete/$', views.delete_user_report), # deletes the user report with the given id
    url(r'^userreports/$', views.list_user_reports), # lists all user reports

    # SPOTIFY
    url(r'^spotify/redirect/$', views.spotify_redirect, name='spotify_redirect'),

    url(r'^user/spotify/authorize/$', views.spotify_authorize, name='spotify_authorize'), # sets up the scope and sends the uri to the Spotify connect page
    url(r'^user/spotify/connect/$', views.spotify_connect, name='spotify_connect'), # connects the Spotify account of the user to his LFC account
    url(r'^user/spotify/disconnect/$', views.spotify_disconnect, name='spotify_disconnect'), # disconnects the account from Spotify
    url(r'^user/spotify/profile/$', views.get_spotify_profile, name='get_spotify_profile'), # returns the Spotify profile of the logged in user.

    url(r'^user/(?P<pk>[0-9]+)/$', views.get_user_with_pk), #returns the user information of the user with the pk as its id
    url(r'^user/(?P<pk>[0-9]+)/follow/$', views.follow_user), # the logged in user follows the one with given pk; requires authorization
    url(r'^user/(?P<pk>[0-9]+)/unfollow/$', views.unfollow_user), # the logged in user unfollows the one with given pk; requires authorization
    url(r'^user/get_concerts/$',views.get_user_concerts), # returns all the concerts of the logged in user; requires authorization
    url(r'^user/(?P<pk>[0-9]+)/get_concerts/$', views.get_user_concerts_with_pk), #returns all the concerts of the user with pk primary key value.
    url(r'^user/deactivate/$', views.deactivate_user, name='deactivate_user'), # deactivates the account of the logged in user; requires authorization
    url(r'^user/delete/$', views.delete_user, name='delete_user'), # deletes the account of a given user; only admins are authorized.
    url(r'^user/delete_all/$', views.delete_all_users, name='delete_all_users'), # deletes all user accounts; only admins are authorized.
    url(r'^user/recommendation_by_followed_users/$', views.get_recommendation_by_followed_users), # recommendations based on followed users
    # CONCERT
    url(r'^concert/(?P<pk>[0-9]+)/subscribe/$', views.subscribe_concert), # subscribes logged in user to the concert; requires authorization
    url(r'^concert/(?P<pk>[0-9]+)/unsubscribe/$', views.unsubscribe_concert), # unsubscribes logged in user from concert; requires authorization
    url(r'^concerts/$', views.list_concerts), # lists all concerts in DB
    url(r'^concerts/get_recommended_concerts/$', views.get_recommendations), #lists the concerts that are recommended to the user using his/her subscribed concerts and spotify top artists if spotify connection is made.
    url(r'^newconcert/$', views.create_concert), # creates a concert with provided info; requires authorization
    url(r'^concert/(?P<pk>[0-9]+)/$', views.concert_detail), # gets, modifies or deletes a specific concert; only admins are authorized for modification or deletion
    url(r'^concert/(?P<reported_concert_id>[0-9]+)/report/$', views.create_concert_report), # creates a concert report for the concert with the given id
    url(r'^concertreports/$', views.list_concert_reports), # lists all concert reports
    url(r'^concertreport/(?P<concert_report_id>[0-9]+)/delete/$', views.delete_concert_report), # deletes the concert report with the given id
    url(r'^concertreport/(?P<concert_report_id>[0-9]+)/upvote/$', views.upvote_concert_report), # upvotes the concert report with the given id
    url(r'^concertreport/(?P<concert_report_id>[0-9]+)/cancel_upvote/$', views.cancel_upvote_concert_report), # cancels the upvote for the concert report with the given id
    # CONCERT SEARCH
    url(r'^concerts/search/$', views.search_concerts), # returns a list of concerts matching with data on their name, location, artist and tags.
    url(r'^concerts/advanced_search/$', views.advanced_search),
    #ARTIST
    url(r'^searchartists/', views.search_artists), # returns a list of artists by doing a search on Spotify given a query string
    # COMMENT
    url(r'^concert/(?P<pk>[0-9]+)/newcomment/$', views.create_comment), # adds a new comment by the logged in user to the concert specified by its primary key; requires authorization
    # RATING
    url(r'^concert/(?P<pk>[0-9]+)/rate/$', views.rate_concert), # adds a new rating by the logged in user to the concert specified by its primary key; requires authorization
    url(r'^concert/(?P<pk>[0-9]+)/average_ratings/$', views.get_average_ratings), # returns the average ratings for the concert specified by its primary key
    # ANNOTATION
    url(r"^list_annotations/$", views.list_annotations), #returns all annotations about a page
    #url(r"^concert/(?P<concert_id>\d+)/annotations/(?P<pk>\d+)$", views.annotation_detail),
    url(r"^new_annotation/$", views.create_annotation), #url for creating new annotation for the concert
    url(r"^annotation/(?P<pk>\d+)/$", views.get_annotation), #returns a specific annotation
    url(r"^annotation/(?P<pk>\d+)/delete/$", views.delete_annotation), #deletes the annotation with pk
    url(r"^all_annotations/$", views.all_annotations),#returns all annotations
    # LOCATION
    url(r'^locations/$',views.list_locations), # lists all locations in DB
    url(r'^location/(?P<pk>[0-9]+)/$',views.location_detail), # gets a specific location in DB
    # TAG
    url(r'^tags/(?P<search_str>[\w\s*\-]+)/$',views.get_tags),
    url(r'^all_tags/$', views.get_all_tags),
    # IMAGE
    url(r'^upload_image/', views.upload_image),


    # REPORT
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ADMIN_ENABLED:
    urlpatterns.append(
        url(r'^admin/', admin.site.urls),
        # .. other stuff you want to be dev-only
        )

urlpatterns.append(
	url(r'^', views.FrontendAppView.as_view()),
	)
