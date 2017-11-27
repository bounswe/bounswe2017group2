from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from lfc_backend.models import RegisteredUser, Concert, Tag, Report, Location, Rating, Comment,  Image, Artist, ConcertImage, UserImage
from lfc_backend.serializers import ConcertSerializer,LocationSerializer, RegisteredUserSerializer, CommentSerializer, RatingSerializer, ImageSerializer, ArtistSerializer
from lfc_backend.forms import ConcertImageForm, UserImageForm
from django.views.generic import FormView, DetailView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.conf import settings

from django.contrib.auth import authenticate, login # for user authentication and login
from django.contrib.auth.decorators import login_required, permission_required # permissions
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q # used in basic search

import spotipy # Lightweight Python library for the Spotify Web API
import traceback
from spotipy.oauth2 import SpotifyClientCredentials # for connecting Spotify when doing artist search


import requests # for sending requests
import json # for getting the response body as json
import re # for regular expressions
import uuid # to generate random string for state in spotify_connect

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework import permissions

#from drf_openapi.views import SchemaView

# class MySchemaView(SchemaView):
#     permission_classes = (permissions.AllowAny, )

# The actual python functions that do the backend work.

'''
USER FUNCTIONS
'''
@api_view(['GET'])
def list_users(request):
    '''
    returns all the registered users
    most recently joined user is at the top
    '''
    #print([f.name for f in RegisteredUser._meta.get_fields()]) # print all user fields for debug
    registered_users = RegisteredUser.objects.all().order_by('-date_joined')
    serializer = RegisteredUserSerializer(registered_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_with_pk(request, pk):
    '''
    returns  the registered user with the given primary key.
    '''
    try:
        user = RegisteredUser.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = RegisteredUserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def follow_user(request,pk):
    '''
    follows the registered user with primary key value pk.
    '''
    if (not request.user.is_authenticated):
        return Response({'Error':'User is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
    me = request.user
    try:
        following_user = RegisteredUser.objects.get(pk=pk) #Following user is the user we wish to follow
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    me.following.add(following_user)
    return Response(status = status.HTTP_200_OK)

@api_view(['POST'])
def unfollow_user(request,pk):
    '''
    unfollows the registered user with primary key value pk.
    '''
    if (not request.user.is_authenticated):
        return Response({'Error':'User is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
    me = request.user
    try:
        unfollowing_user = RegisteredUser.objects.get(pk=pk) #Unfollowing user is the user we wish to unfollow
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    me.following.remove(following_user)
    return Response(status = status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    '''
    registers a new user to the system
    '''
    serializer = RegisteredUserSerializer(data = request.data) # create the user
    if serializer.is_valid():
        # MIGHT ADD SOME REQUIREMENTS FOR PASSWORD.
        # E.G. SHOULD CONTAIN AT LEAST A NUMBER, A CAPITAL AND SMALL LETTER ETC.
        # SIGNUP
        registered_user = serializer.save() # save the user to the database
        return Response(serializer.data, status = status.HTTP_201_CREATED) # success!
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) # something went wrong!

def spotify_get_access_token(user):
    '''
    returns a Spotify access token for the given user
    '''
    client_id = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_id']
    client_secret = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_secret']
    TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
    refresh_token = user.spotify_refresh_token

    params = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token,
        'client_id':client_id,
        'client_secret':client_secret,
    }
    headers = {
         "Content-Type": "application/x-www-form-urlencoded",
     }
    r = requests.post(TOKEN_ENDPOINT, params= params, headers=headers)
    if r.status_code == 200: # SUCCESS!
        return r.json()['access_token']
    else: # the User has taken Looking for Concerts off his applications list in Spotify. Need to disconnect.
        user.spotify_id = None
        user.spotify_display_name = None
        user.spotify_refresh_token = None
        # disconnect this user's account from Spotify
        user.save(update_fields=['spotify_id', 'spotify_display_name','spotify_refresh_token'])
        return {'error':'The user has deleted Looking For Concerts from his \"applications\" in Spotify. He needs to connect his account to Spotify again.', 'status':r.status_code}

@api_view(['GET'])
def get_spotify_profile(request):
    '''
    returns the Spotify profile of the logged in user. Raises an error if the account is not connected to Spotify.
    '''
    if not request.user.is_authenticated:
        return Response({'error':'The user needs to sign in first.'}, status = status.HTTP_401_UNAUTHORIZED)
    elif request.user.spotify_refresh_token is None:
        return Response({'error':'The account is not connected to Spotify.'}, status = status.HTTP_400_BAD_REQUEST)

    result = spotify_get_access_token(request.user)
    if 'error' in result:
        return Response(result['error'], status = result['status'])
    else:
        access_token = result

    print("ACCESS_TOKEN:" + str(access_token))
    sp = spotipy.Spotify(access_token)
    results = sp.current_user()
    return Response(results, status = status.HTTP_200_OK)

# I'm using this to test it without the front-end.
@api_view(['GET'])
def spotify_redirect(request):
    '''
    This endpoint is used for back-end test purposes only.
    '''
    print(request.user.username)
    print(request.session['username'])

    if(request.user.username != request.session['username']):
        return Response({'error':'users do not match'}, status = status.HTTP_401_UNAUTHORIZED)

    print("REDIRECT STATE:" + str(request.GET.get('state')))
    # check state to make sure it is the same user.
    if 'spotify_state' in request.session:
        if request.GET.get('state')==request.session['spotify_state']:
            print("Spotify connect: states matched.")
        else:
            return Response({'error':'states do not match.'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error':'spotify state not found in session.'}, status = status.HTTP_400_BAD_REQUEST)

    if request.GET.get('error') is not None:
        return Response({'error':'The user did not give authorization for connecting to Spotify'}, status = status.HTTP_401_UNAUTHORIZED)

    code = request.GET.get('code') # got the authorization code.

    client_id = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_id']
    client_secret = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_secret']
    #redirect_uri = request.GET.get('redirect_uri') # normally, front-end will provide this as a parameter.
    # Now, since I know the redirect uri I hard coded it.
    redirect_uri = settings.SOCIALACCOUNT_PROVIDERS['spotify']['redirect_uri']

    TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"

    params = {
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : redirect_uri,
        'client_id':client_id,
        'client_secret':client_secret,
    }

    headers = {
         "Content-Type": "application/x-www-form-urlencoded",
     }

    r = requests.post(TOKEN_ENDPOINT, params= params, headers=headers)

    if r.status_code == 200: # SUCCESS!
        spotify_access_token = r.json()['access_token']
        # token type is always "Bearer"
        spotify_refresh_token = r.json()['refresh_token']
        spotify_scope = r.json()['scope']

        print("USERNAME: " + str(request.user.username))
        print("ACCESS TOKEN: " + str(spotify_access_token))
        print("REFRESH TOKEN: " + str(spotify_refresh_token))
        user = request.user
        user.spotify_refresh_token = spotify_refresh_token

        sp = spotipy.Spotify(spotify_access_token)
        spotify_profile = sp.current_user()
        user.spotify_id = spotify_profile['id']
        user.spotify_display_name = spotify_profile['display_name']

        # connect this user's account to Spotify
        user.save(update_fields=['spotify_id', 'spotify_display_name','spotify_refresh_token'])

        return Response({'message':'Successfully connected the account with Spotify!'}, status = status.HTTP_200_OK)
    else:
        Response(status = r.status_code)

# This will be used with the front-end
@api_view(['POST'])
def spotify_connect(request):
    '''
    Connects the account of the logged in user to his Spotify account.
    '''
    print(request.user.username)
    print(request.session['username'])

    if(request.user.username != request.session['username']):
        return Response({'error':'users do not match'}, status = status.HTTP_401_UNAUTHORIZED)

    print("REDIRECT STATE:" + str(request.data['state']))
    # check state to make sure it is the same user.
    if 'spotify_state' in request.session:
        if request.data['state']==request.session['spotify_state']:
            print("Spotify connect: states matched.")
        else:
            return Response({'error':'states do not match.'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error':'spotify state not found in session.'}, status = status.HTTP_400_BAD_REQUEST)

    if request.data['error'] is not None:
        return Response({'error':'The user did not give authorization for connecting to Spotify'}, status = status.HTTP_401_UNAUTHORIZED)

    code = request.data['code'] # got the authorization code.

    client_id = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_id']
    client_secret = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_secret']
    #redirect_uri = request.GET.get('redirect_uri') # normally, front-end will provide this as a parameter.
    # Now, since I know the redirect uri I hard coded it.
    redirect_uri = settings.SOCIALACCOUNT_PROVIDERS['spotify']['redirect_uri']

    TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"

    params = {
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : redirect_uri,
        'client_id':client_id,
        'client_secret':client_secret,
    }

    headers = {
         "Content-Type": "application/x-www-form-urlencoded",
     }

    r = requests.post(TOKEN_ENDPOINT, params= params, headers=headers)

    if r.status_code == 200: # SUCCESS!
        spotify_access_token = r.json()['access_token']
        # token type is always "Bearer"
        spotify_refresh_token = r.json()['refresh_token']
        spotify_scope = r.json()['scope']

        print("USERNAME: " + str(request.user.username))
        print("ACCESS TOKEN: " + str(spotify_access_token))
        print("REFRESH TOKEN: " + str(spotify_refresh_token))
        user = request.user
        user.spotify_refresh_token = spotify_refresh_token

        sp = spotipy.Spotify(spotify_access_token)
        spotify_profile = sp.current_user()
        user.spotify_id = spotify_profile['id']
        user.spotify_display_name = spotify_profile['display_name']

        # connect this user's account to Spotify
        user.save(update_fields=['spotify_id', 'spotify_display_name','spotify_refresh_token'])

        return Response({'message':'Successfully connected the account with Spotify!'}, status = status.HTTP_200_OK)
    else:
        Response(status = r.status_code)


@api_view(['POST'])
def spotify_authorize(request):
    '''
    Returns the Spotify url for the user authorization. If the logged in user denies, his account will not be connected to Spotify.
    Redirect to the returned url.
    You will receive code and state as a response from Spotify if the user gives authorization.
    Else, you will receive error and state as a response.
    Call the user/spotify/connect ENDPOINT with parameters: code/error and state to complete the Spotify connection.
    '''
    if not request.user.is_authenticated:
        return Response({'error':'The user needs to sign in first.'}, status = status.HTTP_401_UNAUTHORIZED)
    elif request.user.spotify_refresh_token is not None:
        return Response({'error':'The account is already connected to Spotify.'}, status = status.HTTP_400_BAD_REQUEST)

    ### STEP 1
    print("building request for Spotify connect step 1...")
    AUTHORIZATION_ENDPOINT = "https://accounts.spotify.com/authorize"
    scope= 'playlist-read-private' # Read access to user's private playlists.
    scope+= ' playlist-read-collaborative' # Include collaborative playlists when requesting a user's playlists.
    scope+= ' user-follow-read' # Read access to the list of artists and other users that the user follows.
    scope+= ' user-library-read' # Read access to a user's "Your Music" library.
    scope+= ' user-read-email' # Read access to user’s email address.
    scope+= ' user-top-read' # Read access to a user's top artists and tracks.

    client_id = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_id']
    client_secret = settings.SOCIALACCOUNT_PROVIDERS['spotify']['client_secret']
    redirect_uri = settings.SOCIALACCOUNT_PROVIDERS['spotify']['redirect_uri']  # redirect URL should normally be the login page.

    # If you generate a random string or encode the hash of some client state (e.g., a cookie)
    # in this state variable, you can validate the response to additionally ensure that the
    # request and response originated in the same browser.
    state = uuid.uuid4().hex
    print("STATE:" +str(state))
    request.session['spotify_state'] = state
    print("SESSION STATE:" +str(request.session['spotify_state']))
    request.session['username']= request.user.username

    params = {
        'client_id' : client_id,
        'response_type' : 'code',
        'redirect_uri' : redirect_uri ,
        'state': state,
        'scope' : scope,
        'show_dialog':False
    }
    print("sending request for Spotify connect step 1...")
    r = requests.get(AUTHORIZATION_ENDPOINT, params = params, allow_redirects=True)
    return Response({'url':r.url},status = r.status_code)


@api_view(['POST'])
def spotify_disconnect(request):
    '''
    Disconnects the account of the logged in user from Spotify.
    '''
    if not request.user.is_authenticated:
        return Response({'error':'The user needs to sign in first.'}, status = status.HTTP_401_UNAUTHORIZED)
    elif request.user.spotify_refresh_token is None:
        return Response({'error':'Cannot disconnect. The account is not connected to Spotify.'}, status = status.HTTP_400_BAD_REQUEST)

    user = request.user
    user.spotify_id = None
    user.spotify_display_name = None
    user.spotify_refresh_token = None
    # disconnect this user's account from Spotify
    user.save(update_fields=['spotify_id', 'spotify_display_name','spotify_refresh_token'])
    return Response({'message':'Account successfully disconnected from Spotify.'},status = status.HTTP_200_OK)

@api_view(['DELETE'])
def deactivate_user(request):
    '''
    deactivates the account of this user
    '''
    if (request.user.is_authenticated):
        pk = request.user.id
        username = request.user.username
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = RegisteredUser.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)

    user.is_active=False
    user.save(update_fields=['is_active'])
    return Response({"message": "Deactivated user " + str(username)},status = status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_user(request):
    '''
    deletes the user with the given username.
    only admins are authorized.
    '''
    if (request.user.is_staff == False):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            username = request.data['username']
            user = RegisteredUser.objects.get(username=username)
        except:
            return Response(status = status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "Deleted user " + str(username)},status = status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_required
def delete_all_users(request):
    '''
    deletes all users
    '''
    if (request.user.is_staff == False):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        print("Deleting all users...")
        try:
            users = RegisteredUser.objects.all()
        except ObjectDoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        users.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_user_info(request):
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = RegisteredUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user_concerts(request):
    '''
    returns all the concerts of a user
    '''
    user = request.user
    if user.is_authenticated:
        concerts=user.concerts.all()
        serializer = ConcertSerializer(concerts, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

'''
CONCERT FUNCTIONS
'''
@api_view(['GET'])
def list_concerts(request):
    '''
    returns all concerts in the system
    @params: None
    '''
    if request.method =='GET':
        concerts = Concert.objects.all().order_by('-date_time') # sort by decreasing date_time
        serializer = ConcertSerializer(concerts, many=True)
        return Response(serializer.data)
    else:
        return status.HTTP_400_BAD_REQUEST

@api_view(['POST'])
def create_concert(request):
    '''
    inserts a concert into the database
    '''
    if (not request.user.is_authenticated):
        return Response({'Error':'User is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)

    # user is logged in at this point
    try:
        artist_data = request.data.pop('artist')
        images_data = artist_data.pop('images')
    except:
        return Response({'Error':'Artist field\'s structure should be identical to the results in searchartist endpoint'},status=status.HTTP_400_BAD_REQUEST)
    artist = None
    #artist lookup in db
    try:
        artist = Artist.objects.get(spotify_id=artist_data['spotify_id'])
    except:
        #artist creation
        try:
            artist_serializer = ArtistSerializer(data = artist_data)
            if artist_serializer.is_valid():
                artist = artist_serializer.save()
                print("2")
        except:
            print("1")
            return Response(artist_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        #images creation and relating with artist
        for image_data in images_data:
            try:
                image_serializer = ImageSerializer(data = image_data)
                if image_serializer.is_valid():
                    image = image_serializer.save()
                    artist.images.add(image) #Exception
            except:
                traceback.print_exc()
                return Response(image_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    #concert creation and relating with artist
    serializer = ConcertSerializer(data = request.data)
    if serializer.is_valid():
        concert = serializer.save()
        artist.concerts.add(concert)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_concerts(request):
    '''
    searches the get data with concerts name, location, artist and tags
    '''
    searchString = request.GET.get('search')
    try:
        concerts = Concert.objects.filter(Q(name__contains=searchString)|
                                          Q(location__venue__contains=searchString)|
                                          Q(artist__name__contains=searchString)|
                                          Q(tags__value__contains=searchString))
        serializer = ConcertSerializer(concerts,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def advanced_search(request):
    '''
    Searches the concerts with the strings given for concert's name, location, artist and tag.
    For each of the fields above, endpoint requires a different string. If string is not given or equal to '' search is not filtered for that field.
    ---For now search can only be done for one tag.
    ---DateTime needs to be implemented
    '''
    data = request.GET
    concert_name = data.get('concert_name','')
    location_venue = data.get('location_venue','')
    artist_name = data.get('artist_name','')
    tag_value = data.get('tag_value','')
    max_value = data.get('max_price','')
    min_value = data.get('min_price','')



    concerts = Concert.objects.all()
    if concert_name !='' :
        concerts = concerts.filter(Q(name__contains=concert_name))
    if location_venue !='' :
        concerts = concerts.filter(Q(location__venue__contains=location_venue))
    if artist_name !='' :
        concerts = concerts.filter(Q(artist__name__contains=artist_name))
    if tag_value !='' :
        concerts = concerts.filter(Q(tags__value__contains=tag_value))
    if max_value.isnumeric() :
        concerts = concerts.filter(Q(price_max__lte=max_value))
    if min_value.isnumeric() :
        concerts = concerts.filter(Q(price_min__gte=min_value))

    try:
        serializer = ConcertSerializer(concerts,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return Response(status = status.HTTP_400_BAD_REQUEST)



# also gets a primary key as a parameter
@api_view(['GET','PUT','DELETE'])
def concert_detail(request, pk):
    '''
    GET: retrieves a concert from the database
    PUT: updates a specific concert in the database
    DELETE: deletes a specific concert from the database
    '''
    try:
        concert = Concert.objects.get(pk=pk) # <-- this pk might be location_id, I'm not sure.
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)

    # returns the concert with the given primary key
    if request.method == 'GET':
        serializer = ConcertSerializer(concert)
        return Response(serializer.data)

    # modifies the concert with the given primary key
    elif request.method == 'PUT':
        serializer = ConcertSerializer(concert, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    # deletes the concert with the given primary key
    elif request.method == 'DELETE':
        concert.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def subscribe_concert(request, pk):
    '''
    adds user to concerts user list
    '''
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        concert = Concert.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    concert.attendees.add(request.user)
    return Response(status  = status.HTTP_200_OK)

@api_view(['POST'])
def unsubscribe_concert(request, pk):
    '''
    removes user from concerts user list
    '''
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        concert = Concert.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    concert.attendees.remove(request.user)
    return Response(status = status.HTTP_204_NO_CONTENT)


'''
ARTIST FUNCTIONS
'''
@api_view(['GET'])
def search_artists(request):
    data = request.GET
    client_credentials_manager = SpotifyClientCredentials(client_id='60ab66df7413492bbc86150d7a3617d7', client_secret='007ccb30ee7e4eb98478b7a34fc869e4')
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    spotifyresults = spotify.search(q='artist:'+data.get('name'), type='artist')
    spotifyresults = spotifyresults['artists']['items']
    results = []
    for spotifyresult in spotifyresults:
        result = {'images':spotifyresult['images'], 'spotify_id':spotifyresult['id'], 'name':spotifyresult['name']}
        results.append(result)
    return Response(results, status = status.HTTP_200_OK)

'''
LOCATION FUNCTIONS
'''
@api_view(['GET'])
def list_locations(request):
    '''
    returns all locations
    @params: None
    '''
    if request.method =='GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    else:
        return status.HTTP_400_BAD_REQUEST

@api_view(['GET'])
def location_detail(request, pk):
    try:
        location = Location.objects.get(pk=pk) # <-- this pk might be location_id, I'm not sure. <--- It is
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = LocationSerializer(location)
    return Response(serializer.data)

'''
RATING FUNCTIONS
'''

@api_view(['POST'])
def rate_concert(request,pk):
    '''
    Adds ratings by the logged in user to the concert with given pk
    @params
    '''
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        concert = Concert.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    try:
        concert.attendees.get(pk=request.user.pk)
    except:
        return Response(status = status.HTTP_403_FORBIDDEN)

    try: # if this user has already rated this concert
        rating = concert.ratings.get(concert = concert.pk, owner = request.user.pk)
        serializer = RatingSerializer(rating, data = request.data)
        if serializer.is_valid():
            rating = serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist: # if this user is rating this concert for the first time
        serializer = RatingSerializer(data = request.data)
        if serializer.is_valid():
            rating = serializer.save()
            request.user.concert_ratings.add(rating)
            concert.ratings.add(rating)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


'''
TAG FUNCTIONS
'''

@api_view(['GET'])
def get_tags(request, search_str):
    '''
    @param: search_str
    @return: json list of tags found
    '''
    if (not request.user.is_authenticated):
        return Response({'Error':'User is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)

    API_ENDPOINT = "https://www.wikidata.org/w/api.php"
    query = search_str
    params = {
        'action' : 'wbsearchentities',
        'format' : 'json',
        'language' : ['en', 'tr'],
        'search' : query,
        'type'   :'item'
    }

    r = requests.get(API_ENDPOINT, params = params)
    json_response = r.json()['search']
    lenght =  len(json_response)
    #print(json_response)
    
    tags = []
    for i in range(lenght):
        if 'description' in json_response[i]:
            if any(re.findall(r'music|genre', json_response[i]['description'], re.IGNORECASE)):
                value   = json_response[i]['label']
                context = json_response[i]['description']
                url     = json_response[i]['concepturi']
                t = '{"value":"'+value.replace('"','')+ '","context":"' + context.replace('"','') + '","uri":"' + url.replace('"','') + '"}'
                print(t)
                tags.append(json.loads(t))

    return Response(tags, status.HTTP_200_OK)

'''
COMMENT FUNCTIONS
'''

@api_view(['POST'])
def create_comment(request,pk):
    '''
    Adds a comment by the logged in user to the concert with given pk
    '''
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        concert = Concert.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data = request.data)
    serializer.is_valid()
    comment = serializer.save()
    request.user.comments.add(comment)
    concert.comments.add(comment)
    return Response(serializer.data)

'''
IMAGE FUNCTIONS
'''
class ConcertImageView(FormView):
    '''
    Uploads a concert image to the database
    @return: url of the uploaded image
    '''
    template_name = 'concert_image_form.html'
    form_class = ConcertImageForm

    def form_valid(self, form):
        concert_image = ConcertImage(
            image=self.get_form_kwargs().get('files')['image'])
        concert_image.save()
        self.id = concert_image.id
        return HttpResponse(concert_image.image.url)

@api_view(['GET'])
def ConcertShowImage(request, pk):
    '''
    @param: pk, id of the cocert image
    @return: url of that image
    '''
    img = ConcertImage.objects.get(pk=pk)
    return HttpResponseRedirect(concert_image.image.url)

class UserImageView(FormView):
    '''
    Uploads a user image to the database
    @return: url of the uploaded image
    '''
    template_name = 'user_image_form.html'
    form_class = UserImageForm

    def form_valid(self, form):
        user_image = UserImage(
            image=self.get_form_kwargs().get('files')['image'])
        user_image.save()
        self.id = user_image.id
        return HttpResponse(user_image.image.url)

@api_view(['GET'])
def UserShowImage(request, pk):
    '''
    @param: pk, id of the user image
    @return: url of the image
    '''
    img = UsserImage.objects.get(pk=pk)
    return HttpResponseRedirect(user_image.image.url)
