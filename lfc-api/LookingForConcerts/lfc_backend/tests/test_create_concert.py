from django.test.client import Client
from django.test import TestCase
from rest_framework.test import APIClient # for login
import json
import pytest
import requests
from rest_framework_simplejwt import authentication
from lfc_backend.serializers import RegisteredUserSerializer
from datetime import timedelta
from datetime import datetime
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed, InvalidToken
)
import time
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import pprint

@pytest.mark.django_db
class SearchArtistTestCase(TestCase):
    def setUp(self):
        self.artistName = 'Tarkan'
        self.artistSearchUrl = '/searchartists/'
        self.client = Client()
    
    def test_search_artist_with_valid_info(self):
        data = {'name': self.artistName}
        response = self.client.get(self.artistSearchUrl,data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Tarkan')

    def test_search_artist_without_info(self):
        response = self.client.get(self.artistSearchUrl)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'You need to give an artist name.')

@pytest.mark.django_db
class SearchTagTestCase(TestCase):
    def setUp(self):
        self.login_url = '/login/'
        self.username = 'HalukAlper'
        self.password = 'looking4C'
        self.email = 'halukalper@gmail.com'
        self.credentials = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
        }
        self.tagValue = 'Turkish'
        self.artistSearchUrl = '/tags/'
        serializer = RegisteredUserSerializer(data=self.credentials)
        if serializer.is_valid():
            self.user = serializer.save()
        self.client = Client()
        response = self.client.post(self.login_url,{'username':self.username, 'password':self.password})
        self.authorization = 'Bearer ' + response.data['access']

    def test_search_tags_with_valid_info(self):
        url = self.artistSearchUrl + self.tagValue + '/'
        result = {
            "value": "Turkish Republic of Northern Cyprus",
            "context": "self-declared state",
            "wikidata_uri": "http://www.wikidata.org/entity/Q23681"
        }
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0],result)

    def test_search_tags_with_unregistered_user(self):
        url = self.artistSearchUrl + self.tagValue + '/'
        newClient = Client()
        response = newClient.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['Error'], 'User is not authenticated')

@pytest.mark.django_db
class CreateConcertTestCase(TestCase):

    def setUp(self):
        self.username = 'HalukAlper'
        self.password = 'looking4C'
        self.email = 'halukalper@gmail.com'
        self.credentials = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
        }
        serializer = RegisteredUserSerializer(data=self.credentials)
        if serializer.is_valid():
            self.user = serializer.save()
        self.login_url = '/login/'
        self.createConcertUrl = '/newconcert/'
        self.concertName = 'MFÖ Yılbaşı Konseri'
        self.date_time = '2017-12-31'
        self.artist = {
            "name": "MFÖ",
            "spotify_id": "2jbrqAuwSdvwcMTbtvncND",
            "images": [
                {
                    "url": "https://i.scdn.co/image/7f30f27e4cce2a13b19e23024e01f70494f181db",
                    "height": 640,
                    "width": 640
                },
                {
                    "url": "https://i.scdn.co/image/13924cb4f291d71839b47c54b2c1145f875e780c",
                    "height": 300,
                    "width": 300
                },
                {
                    "url": "https://i.scdn.co/image/ca0bd7579cf4c191fc5fa7534b6654786a9ef4e1",
                    "height": 64,
                    "width": 64
                }
            ]
        }
        self.description = "Müzik sahnemizin efsanevi grubu Mazhar Fuat Özkan (MFÖ), 31 Aralık’ta Atlantis iş birliğiyle gerçekleştirilen Vestel #gururlayerli konserleri kapsamında Zorlu PSM'de olacak!"
        self.price_min = 60
        self.price_max = 150
        self.tags =[
            {
                "value": "pop music",
                "context": "genre of popular music which originated in its modern form in the late-1950s, deriving from rock and roll",
                "wikidata_uri": "http://www.wikidata.org/entity/Q37073"
            },
            {
                "value": "Istanbul",
                "context": "largest city in Turkey",
                "wikidata_uri": "http://www.wikidata.org/entity/Q406"
            }
        ]
        self.location = {
            "venue": "Zorlu PSM - Ana Tiyatro",
            "coordinates": "41.0660865 29.0174246"
        }
        self.seller_url = "www.biletix.com/etkinlik/V1T01/TURKIYE/tr"
        #Log in the test user
        self.client = Client()
        response = self.client.post(self.login_url,{'username':self.username, 'password':self.password})
        self.authorization = 'Bearer ' + response.data['access']

    def test_create_concert_with_valid_info(self):
        """
        Ensure concert is being created with valid info
        """
        info = {
            "name": self.concertName,
            "artist": self.artist,
            "date_time": self.date_time,
            "description": self.description,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "tags": self.tags,
            "location": self.location,
            "seller_url": self.seller_url
        }
        response = self.client.post(
                 self.createConcertUrl,
                 json.dumps(info),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.authorization
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], info['name'])
        self.assertEqual(response.data['date_time'], info['date_time'])
        self.assertEqual(response.data['description'], info['description'])
        self.assertEqual(response.data['price_min'], info['price_min'])
        self.assertEqual(response.data['price_max'], info['price_max'])


    def test_create_concert_without_artist(self):
        """
        Ensure that create concert does not work without artist info.
        """
        info = {
            "name": self.concertName,
            "date_time": self.date_time,
            "description": self.description,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "tags": self.tags,
            "location": self.location,
            "seller_url": self.seller_url
        }
        response = self.client.post(
                 self.createConcertUrl,
                 json.dumps(info),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.authorization
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'],'Artist field\'s structure should be identical to the results in searchartist endpoint')

    def test_create_concert_without_location(self):
        """
        Ensure that create concert does not work without location info.
        """
        info = {
            "name": self.concertName,
            "artist": self.artist,
            "date_time": self.date_time,
            "description": self.description,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "tags": self.tags,
            "seller_url": self.seller_url
        }
        response = self.client.post(
                 self.createConcertUrl,
                 json.dumps(info),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.authorization
             )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['location'], ['This field is required.'])

    def test_create_concert_with_unregistered_user(self):
        """
        Ensure that create concert url gives error when an unauthorized user tries to create a concert
        """
        info = {
            "name": self.concertName,
            "artist": self.artist,
            "date_time": self.date_time,
            "description": self.description,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "tags": self.tags,
            "location": self.location,
            "seller_url": self.seller_url
        }
        newClient = Client()
        response = newClient.post(
            self.createConcertUrl,
            json.dumps(self.credentials),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401) # unauthorized
        self.assertEqual(response.data['Error'],'User is not authenticated') # got an access token
        

    def test_create_concert_with_same_date_and_artist(self):
        """
        Ensure that two concerts with same date and artist could not be created
        """
        info1 = {
            "name": self.concertName,
            "artist": self.artist,
            "date_time": self.date_time,
            "description": self.description,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "tags": self.tags,
            "location": self.location,
            "seller_url": self.seller_url
        }

        location2 = {
            "venue": "Different Location",
            "coordinates": "41.0660865 29.0174246"
        }
        info2 = {
            "name": "different concert name",
            "artist": self.artist,
            "date_time": self.date_time,
            "description": "different description",
            "price_min": 9990,
            "price_max": 10000,
            "tags": self.tags, #Tags does not matter
            "location": location2,
            "seller_url": "different seller url"
        }

        #Create first concert
        self.client.post(
            self.createConcertUrl,
            json.dumps(info1),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.authorization
        )

        #Try to create second concert
        response = self.client.post(
            self.createConcertUrl,
            json.dumps(info2),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.authorization    
        )

        self.assertEqual(response.status_code, 400) # fail
        self.assertEqual(response.data['Error'], 'An artist can not have more than one concert in one day.')