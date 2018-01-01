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
class RecommendationTestCase(TestCase):
    def setUp(self):
        self.username1 = 'HalukAlper'
        self.password1 = 'looking4C'
        self.username2 = 'Kubilay'
        self.password2 = 'LFCZLYH'
        self.email1 = 'halukalper@gmail.com'
        self.email2 = 'kubilay@gmail.com'
        self.credentials1 = {
            'username': self.username1,
            'password': self.password1,
            'email': self.email1,
        }
        self.credentials2 = {
            'username': self.username2,
            'password': self.password2,
            'email': self.email2,
        }
        serializer = RegisteredUserSerializer(data=self.credentials1)
        if serializer.is_valid():
            self.user = serializer.save()
        serializer = RegisteredUserSerializer(data=self.credentials2)
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
        self.date_time2 = '2018-01-31'
        self.artist2 = {
            "name": "Metallica 2",
            "spotify_id": "2ye2Wgw4gimLv2eAKyk1NB",
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

        #CONCERT 3
        self.concertName3 = "Metallica2"
        self.date_time3 = '2019-12-31'
        self.artist3 = {
            "name": "Metallica",
            "spotify_id": "2ye2Wgw4gimLv2eAKyk1NB",
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
        self.description3 = "Metallica is an American heavy metal band from Los Angeles, California. The band was formed in 1981 by drummer Lars Ulrich and vocalist/guitarist James Hetfield. The band's fast tempos, instrumentals and aggressive musicianship made them one of the founding \"big four\" bands of thrash metal, alongside Megadeth, Anthrax and Slayer. Metallica's current lineup comprises founding members Hetfield and Ulrich, longtime lead guitarist Kirk Hammett and bassist Robert Trujillo. Guitarist Dave Mustaine (who formed Megadeth) and bassists Ron McGovney, Cliff Burton and Jason Newsted are former members of the band."
        self.price_min3 = 100
        self.price_max3 = 300
        self.tags3 = []
        self.location3 = {
            "venue": "Şükrü Saracoğlu",
            "coordinates": "40.9876894 29.0365648"
        }
        self.seller_url3 = "www.metallica.com/tour"

        #CONCERT 4
        self.concertName4 = 'JJJ Concert'
        self.date_time4 = '2018-12-31'
        self.artist4 = {
            "images": [
                {
                    "height": 1319,
                    "url": "https://i.scdn.co/image/bf76acee65dac1e84fcdaca93e3e2015a763ba71",
                    "width": 1000
                },
                {
                    "height": 844,
                    "url": "https://i.scdn.co/image/907f3e41c42e4000650c1c4224471e3d93df1e6a",
                    "width": 640
                },
                {
                    "height": 264,
                    "url": "https://i.scdn.co/image/ee643f9e92be38f28e86e24a25119a55ea945435",
                    "width": 200
                },
                {
                    "height": 84,
                    "url": "https://i.scdn.co/image/bbad8e229b94096d5b3e44ea798abffb5976d7c0",
                    "width": 64
                }
            ],
            "spotify_id": "4hzC9WUUy3cFituT71tzB4",
            "name": "Jay-Jay Johanson"
        }
        self.description4 = "Müzik sahnelerinin efsanevi sanatçısı JJ Johanson, 31 Aralık’ta Atlantis iş birliğiyle gerçekleştirilen Vestel #gururlayerli konserleri kapsamında IKSV'de olacak!"
        self.price_min4 = 60
        self.price_max4 = 150
        self.tags4 =[
            {
                "value": "Istanbul",
                "context": "largest city in Turkey",
                "wikidata_uri": "http://www.wikidata.org/entity/Q406"
            }
        ]
        self.location4 = {
            "venue": "IKSV",
            "coordinates": "40.9876894 29.0365648"
        }
        self.seller_url4 = "www.biletix.com/etkinlik/V1T01/TURKIYE/tr"


        #Log in the test user
        self.client = Client()
        response = self.client.post(self.login_url,{'username':self.username1, 'password':self.password1})
        self.UserAuthorization1 = 'Bearer ' + response.data['access']
        response = self.client.post(self.login_url,{'username':self.username2, 'password':self.password2})
        self.UserAuthorization2 = 'Bearer ' + response.data['access']
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
        info3 = {
            "name": self.concertName3,
            "artist": self.artist3,
            "date_time": self.date_time3,
            "description": self.description3,
            "price_min": self.price_min3,
            "price_max": self.price_max3,
            "tags": self.tags3,
            "location": self.location3,
            "seller_url": self.seller_url3
        }
        info4 = {
            "name": self.concertName4,
            "artist": self.artist4,
            "date_time": self.date_time4,
            "description": self.description4,
            "price_min": self.price_min4,
            "price_max": self.price_max4,
            "tags": self.tags4,
            "location": self.location4,
            "seller_url": self.seller_url4
        }

        self.client.post(
                 self.createConcertUrl,
                 json.dumps(info1),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.UserAuthorization1
        )
        self.client.post(
                 self.createConcertUrl,
                 json.dumps(info2),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.UserAuthorization1
        )
        self.client.post(
                 self.createConcertUrl,
                 json.dumps(info3),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.UserAuthorization1
        )
        self.client.post(
                 self.createConcertUrl,
                 json.dumps(info4),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.UserAuthorization1
        )
        self.client.post('/concert/1/subscribe/',HTTP_AUTHORIZATION = self.UserAuthorization2)
    
    def test_recommendation_from_followed_user(self):
        #user1 follows user2. Therefore gets the concerts of the user2's attending as recommendations
        self.client.post('/user/2/follow/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        response = self.client.get('/concerts/get_recommended_concerts/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'MFÖ Yılbaşı Konseri')
        self.assertEqual(len(response.data), 1)

    def test_recommendation_from_watched_artist(self):
        #User subscribes to Metallica concert
        self.client.post('/concert/2/subscribe/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        response = self.client.get('/concerts/get_recommended_concerts/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Metallica2')
        self.assertEqual(len(response.data), 1)

    def test_recommendation_from_same_tags(self):
        #User subscribes to Mfö concert, jay jay concert also have istanbul tag, therefore it is recommended
        self.client.post('/concert/1/subscribe/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        response = self.client.get('/concerts/get_recommended_concerts/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'JJJ Concert')
        self.assertEqual(len(response.data), 1)

    def test_recommendation_orders_watched_artist_then_followed_user(self):
        #Recommendations from watched artists have precedence over 1 followed user recommendations
        self.client.post('/concert/2/subscribe/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        self.client.post('/user/2/follow/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        response = self.client.get('/concerts/get_recommended_concerts/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Metallica2')
        self.assertEqual(response.data[1]['name'], 'MFÖ Yılbaşı Konseri')
        self.assertEqual(len(response.data), 2)

    def test_not_getting_already_subscribed_concerts(self):
        #Already subscribed concerts are not in recommended concerts
        self.client.post('/concert/1/subscribe/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        self.client.post('/concert/4/subscribe/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        response = self.client.get('/concerts/get_recommended_concerts/', HTTP_AUTHORIZATION = self.UserAuthorization1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
    




    