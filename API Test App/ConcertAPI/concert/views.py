# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from concert.models import Concert,User
from concert.serializers import ConcertSerializer, UserSerializer

import unittest


# Create your views here.
@csrf_exempt
def concert_list(request):
    """
        List all concerts, or create a new concert.
        """
    if request.method == 'GET':
        concerts = Concert.objects.all()
        serializer = ConcertSerializer(concerts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ConcertSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def concert_detail(request, pk):
    """
        Retrieve, update or delete a concert.
        """
    try:
        concert = Concert.objects.get(pk=pk)
    except Concert.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ConcertSerializer(concert)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ConcertSerializer(concert, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        concert.delete()
        return HttpResponse(status=204)
    
    # Create your views here.
@csrf_exempt
def user_list(request):
    """
        List all users, or create a new user.
        """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user_detail(request, pk):
    """
        Retrieve, update or delete a user.
        """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)
