from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from lfc_backend.models import RegisteredUser, Concert, Tag, Report, Location, Rating, Comment,  Image, Artist
from lfc_backend.serializers import ConcertSerializer,LocationSerializer, RegisteredUserSerializer, CommentSerializer, RatingSerializer, ImageSerializer, ArtistSerializer

from django.contrib.auth import authenticate, login # for user authentication and login
from django.contrib.auth import logout # for user logout
from django.contrib.auth.decorators import login_required, permission_required # permissions
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
import spotipy
import traceback
import json
from spotipy.oauth2 import SpotifyClientCredentials

# The actual python functions that do the backend work.

'''
TOKEN FUNCTIONS
'''

@api_view(['POST'])
def get_token(request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(request, username=email, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

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

@api_view(['GET'])
def user_detail(request,pk):
    '''
    returns all the registered users
    most recently joined user is at the top
    '''
    registered_users = RegisteredUser.objects.get(pk=pk)
    serializer = RegisteredUserSerializer(registered_users)
    return Response(serializer.data)

@api_view(['POST'])
def signup(request):
    '''
    registers a new user to the system
    '''
    serializer = RegisteredUserSerializer(data = request.data) # create the user
    if serializer.is_valid():
        # SIGNUP
        registered_user = serializer.save() # save the user to the database
        # LOGIN
        email = registered_user.email # username
        password = request.data['password'] # unhashed password that the user entered
        user = authenticate(username=email, password=password) # authenticate() hashes the given function inside before checking
        login(request,user) # log in the user right after signup
        return Response(serializer.data, status = status.HTTP_201_CREATED) # success!
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) # something went wrong!

@api_view(['DELETE'])
@permission_required
def delete_user(request,pk):
    '''
    deletes the user with the given primary key
    '''
    try:
        user = RegisteredUser.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_required
def delete_all_users(request):
    '''
    deletes all users
    '''
    print("Deleting all users...")
    try:
        users = RegisteredUser.objects.all()
    except ObjectDoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    users.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def registered_user_login(request):
    '''
    logs in the user to the system
    '''
    email = request.data['email']
    password = request.data['password'] # unhashed password that the user entered
    print(email, password)
    user = authenticate(request, username=email, password=password) # authenticate() hashes the given function inside before checking

    if user is not None:
        if user.is_active:
                request.session.set_expiry(86400) #sets the exp. value of the session
                print("logged in.")
                # Redirect to a success page.
                serializer = RegisteredUserSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                data = serializer.data
                data['token'] = token.key

                return Response(data,status=status.HTTP_200_OK)
        else:
            print("User profile has been deleted.")
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        print("invalid login")
        return Response(status=status.HTTP_400_BAD_REQUEST)
        # Return an 'invalid login' error message.

@api_view(['POST'])
def registered_user_logout(request):
    '''
    logs out the user
    '''
    logout(request)
    print("Logged out.")
    return Response(status=status.HTTP_200_OK)
    # Redirect to a success page.


@api_view(['GET'])
def get_logged_in_user(request):
    user = request.user
    return Response(user,status=status.HTTP_200_OK)

'''
CONCERT FUNCTIONS
'''

@api_view(['GET'])
def list_concerts(request):
    '''
    returns all concerts
    @params: None
    '''
    if request.method =='GET':
        concerts = Concert.objects.all()
        serializer = ConcertSerializer(concerts, many=True)
        return Response(serializer.data)
    else:
        return status.HTTP_400_BAD_REQUEST

@api_view(['POST'])
#@login_required()
#@permission_required('IsAuthenticated')
def create_concert(request):
    '''
    inserts a concert into the database
    '''
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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

@api_view(['GET'])
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
    concert.users.add(request.user)
    return Response(status  = status.HTTP_200_OK)

@api_view(['GET'])
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
    concert.users.remove(request.user)
    return Response(status  = status.HTTP_204_NO_CONTENT)


'''
ARTIST FUNCTIONS
'''
@api_view(['POST'])
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
    # returns the concert with the given primary key
    serializer = LocationSerializer(location)
    return Response(serializer.data)

'''
RATING FUNCTIONS
'''

@api_view(['POST'])
def rate_concert(request,pk):
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        concert = Concert.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    try:
        concert.users.get(pk=request.user.pk)
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
COMMENT FUNCTIONS
'''

@api_view(['POST'])
def create_comment(request,pk):
    if (not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        concert = Concert.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data = request.data)
    serializer.is_valid()
    #comment = serializer.save(owner = request.user)
    comment = serializer.save()
    request.user.comments.add(comment)
    concert.comments.add(comment)
    return Response(serializer.data)
