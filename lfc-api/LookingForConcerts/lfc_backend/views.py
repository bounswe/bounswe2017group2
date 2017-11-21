from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from lfc_backend.models import RegisteredUser, Concert, Tag, Report, Location, Rating, Comment,  Image, Artist
from lfc_backend.serializers import ConcertSerializer,LocationSerializer, RegisteredUserSerializer, CommentSerializer, RatingSerializer, ImageSerializer, ArtistSerializer

from django.contrib.auth import authenticate, login # for user authentication and login
from django.contrib.auth.decorators import login_required, permission_required # permissions
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import spotipy
import traceback
import json
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json
import re

from rest_framework_simplejwt.tokens import RefreshToken # for blacklisting tokens upon user logout

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

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
    print([f.name for f in RegisteredUser._meta.get_fields()]) # print all user fields for debug
    registered_users = RegisteredUser.objects.all().order_by('-date_joined')
    serializer = RegisteredUserSerializer(registered_users, many=True)
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
        serializer = ConcertSerializer(concerts)
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
        concerts = Concert.objects.all()
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
    artist_data = request.data.pop('artist')
    images_data = artist_data.pop('images')
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
    searches the post data with concerts name, location, artist and tags
    '''
    searchString = request.data['search']
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
    data = request.data
    client_credentials_manager = SpotifyClientCredentials(client_id='60ab66df7413492bbc86150d7a3617d7', client_secret='007ccb30ee7e4eb98478b7a34fc869e4')
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    spotifyresults = spotify.search(q='artist:'+data['name'], type='artist')
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

    try:
        rating = concert.ratings.get(concert = concert.pk, owner = request.user.pk)
        serializer = RatingSerializer(rating, data = request.data)
        if serializer.is_valid():
            rating = serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
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
    if (not request.user.is_authenticated):
        return Response({'Error':'User is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)

    API_ENDPOINT = "https://www.wikidata.org/w/api.php"
    query = search_str
    params = {
        'action' : 'wbsearchentities',
        'format' : 'json',
        'language' : ['en', 'tr'],
        'search' : query,
        'type':'item'
    }

    r = requests.get(API_ENDPOINT, params = params)
    json_response = r.json()['search']
    lenght =  len(json_response)

    tags = []
    for i in range(lenght):
        if 'description' in json_response[i]:
            if any(re.findall(r'music|genre', json_response[i]['description'], re.IGNORECASE)):
                value = json_response[i]['label']
                context = json_response[i]['description']
                t = '{"value":"'+value.replace('"','')+ '","context":"'+context.replace('"','')+'"}'
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
