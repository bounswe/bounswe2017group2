from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from lfc_backend.models import Concert, Tag, Report, Location, Rating, Comment
from lfc_backend.serializers import ConcertSerializer,LocationSerializer, RegisteredUserSerializer, CommentSerializer

from django.contrib.auth import authenticate, login # for user authentication and login
from django.contrib.auth import logout # for user logout
from django.contrib.auth.decorators import login_required, permission_required # permissions

# Organized according to tutorial 2 in django-rest-framework with using models.py and serializer.py

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
#@login_required
#@permission_required('lfc_backend.can_create_concert', raise_exception=True)
def create_concert(request):
    '''
    inserts a concert into the database
    '''
    if request.method =='POST':
        serializer = ConcertSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    else:
        return status.HTTP_400_BAD_REQUEST

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

# takes no parameters
@api_view(['GET'])
def list_users(request):
    '''
    returns all registered users
    '''
    registered_users = User.objects.all()
    serializer = RegisteredUserSerializer(registered_users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user():
    '''
    inserts a user into the database
    '''
    serializer = RegisteredUserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def registered_user_login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.

    else:
        print("invalid login")
        # Return an 'invalid login' error message.

def registered_user_logout(request):
    logout(request)
    # Redirect to a success page.

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
        location = Location.objects.get(pk=pk) # <-- this pk might be location_id, I'm not sure.
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    # returns the concert with the given primary key
    serializer = LocationSerializer(location)
    return Response(serializer.data)

@api_view(['POST']) 
def comment_create(request,pk):
    try:
        concert = Concert.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data = request.data)
    serializer.is_valid()
    comment = serializer.save()
    concert.comments.add(comment)
    return Response(serializer.data)
    #need session data of the current user to relate the comment to him/her.
    
        
