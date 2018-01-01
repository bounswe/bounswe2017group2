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
        self.advancedSearchUrl = '/concerts/advanced_search/'
        #CONCERT 1
        self.concertName1 = 'MFÖ Yılbaşı Konseri'
        self.date_time1 = '2017-12-31'
        self.artist1 = {
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
        self.description1 = "Müzik sahnemizin efsanevi grubu Mazhar Fuat Özkan (MFÖ), 31 Aralık’ta Atlantis iş birliğiyle gerçekleştirilen Vestel #gururlayerli konserleri kapsamında Zorlu PSM'de olacak!"
        self.price_min1 = 60
        self.price_max1 = 150
        self.tags1 =[
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
        self.location1 = {
            "venue": "Şükrü Saracoğlu",
            "coordinates": "40.9876894 29.0365648"
        }
        self.seller_url1 = "www.biletix.com/etkinlik/V1T01/TURKIYE/tr"

        #CONCERT 2
        self.concertName2 = "Metallica"
        self.date_time2 = '2017-12-31'
        self.artist2 = {
            "name": "Metallica",
            "spotify_id": "2ye2Wgw4gimLv2eAKyk1NB",
            "concerts": [
                13,
                17
            ],
            "images": [
                {
                    "url": "https://i.scdn.co/image/5a06711d7fc48d5e0e3f9a3274ffed3f0af1bd91",
                    "height": 640,
                    "width": 640
                },
                {
                    "url": "https://i.scdn.co/image/0c22030833eb55c14013bb36eb6a429328868c29",
                    "height": 320,
                    "width": 320
                },
                {
                    "url": "https://i.scdn.co/image/c1fb4d88de092b5617e649bd4c406b5cab7d3ddd",
                    "height": 160,
                    "width": 160
                }
            ]
        }
        self.description2 = "Metallica is an American heavy metal band from Los Angeles, California. The band was formed in 1981 by drummer Lars Ulrich and vocalist/guitarist James Hetfield. The band's fast tempos, instrumentals and aggressive musicianship made them one of the founding \"big four\" bands of thrash metal, alongside Megadeth, Anthrax and Slayer. Metallica's current lineup comprises founding members Hetfield and Ulrich, longtime lead guitarist Kirk Hammett and bassist Robert Trujillo. Guitarist Dave Mustaine (who formed Megadeth) and bassists Ron McGovney, Cliff Burton and Jason Newsted are former members of the band."
        self.price_min2 = 100
        self.price_max2 = 300
        self.tags2 = [
            {
                "value": "Metallica",
                "context": "American Rock &Roll band",
                "wikidata_uri": "http://www.wikidata.org/entity/Q15920"
            },
            {
                "value": "hard rock",
                "context": "genre of rock music often characterized by guitar riffs accompanied by root notes on the bass guitar and big drums",
                "wikidata_uri": "http://www.wikidata.org/entity/Q83270"
            }
        ]
        self.location2 = {
            "venue": "Şükrü Saracoğlu",
            "coordinates": "40.9876894 29.0365648"
        }
        self.seller_url2 = "www.metallica.com/tour"
        #Log in the test user
        self.client = Client()
        response = self.client.post(self.login_url,{'username':self.username, 'password':self.password})
        self.authorization = 'Bearer ' + response.data['access']
        #Create the concerts
        info1 = {
            "name": self.concertName1,
            "artist": self.artist1,
            "date_time": self.date_time1,
            "description": self.description1,
            "price_min": self.price_min1,
            "price_max": self.price_max1,
            "tags": self.tags1,
            "location": self.location1,
            "seller_url": self.seller_url1
        }
        info2 = {
            "name": self.concertName2,
            "artist": self.artist2,
            "date_time": self.date_time2,
            "description": self.description2,
            "price_min": self.price_min2,
            "price_max": self.price_max2,
            "tags": self.tags2,
            "location": self.location2,
            "seller_url": self.seller_url2
        }
        self.client.post(
                 self.createConcertUrl,
                 json.dumps(info1),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.authorization
        )
        self.client.post(
                 self.createConcertUrl,
                 json.dumps(info2),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.authorization
        )

    def test_advanced_search_by_concert_name(self):
        response = self.client.get(self.advancedSearchUrl,{'concert_name':'Metallica'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'],'Metallica')
        self.assertEqual(len(response.data),1)

    def test_advanced_search_by_location_name(self):
        response = self.client.get(self.advancedSearchUrl,{'location_venue':'Şükrü'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),2)

    def test_advanced_search_by_artist_name(self):
        response = self.client.get(self.advancedSearchUrl,{'artist_name':'MFÖ'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'],'MFÖ Yılbaşı Konseri')
        self.assertEqual(len(response.data),1)

    def test_advanced_search_by_tag_value(self):
        response = self.client.get(self.advancedSearchUrl,{'tag_value':'hard rock'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'],'Metallica')
        self.assertEqual(len(response.data),1)

    def test_advanced_search_by_max_price(self):
        response = self.client.get(self.advancedSearchUrl,{'max_price': 180})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'],'MFÖ Yılbaşı Konseri')
        self.assertEqual(len(response.data),1)
    
    def test_advanced_search_by_min_price(self):
        response = self.client.get(self.advancedSearchUrl,{'min_price': 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),2)

    def test_advanced_search_with_two_parameters(self):
        response = self.client.get(self.advancedSearchUrl,{'min_price': 50, 'tag_value':'Istanbul'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'],'MFÖ Yılbaşı Konseri')
        self.assertEqual(len(response.data),1)