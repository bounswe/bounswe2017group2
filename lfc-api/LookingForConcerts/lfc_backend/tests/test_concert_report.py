from django.test.client import Client
from django.test import TestCase
from rest_framework.test import APIClient # for login
import json
import pytest
import requests
from rest_framework_simplejwt import authentication
from lfc_backend.serializers import RegisteredUserSerializer, ArtistSerializer
from datetime import timedelta
from datetime import datetime
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed, InvalidToken
)
import time
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from lfc_backend.models import Concert, ConcertReport, Artist
import pprint

@pytest.mark.django_db
class ConcertReportTestCase(TestCase):
    def setUp(self):
        self.username1 = 'kemalberk'
        self.password1 = 'looking4C'
        self.email1 = 'kberk@gmail.com'

        self.username2 = 'user2'
        self.password2 = 'user2'
        self.email2 = 'user2@gmail.com'

        self.username3 = 'user3'
        self.password3 = 'user3'
        self.email3 = 'user3@gmail.com'

        self.username4 = 'user4'
        self.password4 = 'user4'
        self.email4 = 'user4@gmail.com'


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

        self.credentials3 = {
            'username': self.username3,
            'password': self.password3,
            'email': self.email3,
        }

        self.credentials4 = {
            'username': self.username4,
            'password': self.password4,
            'email': self.email4,
        }

        serializer = RegisteredUserSerializer(data=self.credentials1)
        if serializer.is_valid():
            self.user1 = serializer.save()
        serializer = RegisteredUserSerializer(data=self.credentials2)
        if serializer.is_valid():
            self.user2 = serializer.save()
        serializer = RegisteredUserSerializer(data=self.credentials3)
        if serializer.is_valid():
            self.user3 = serializer.save()
        serializer = RegisteredUserSerializer(data=self.credentials4)
        if serializer.is_valid():
            self.user4 = serializer.save()

        self.login_url = '/login/'
        self.createConcertUrl = '/newconcert/'

        #Log in the test user
        self.client = Client()
        response = self.client.post(self.login_url,{'username':self.username1, 'password':self.password1})
        self.UserAuthorization1 = 'Bearer ' + response.data['access']
        response = self.client.post(self.login_url,{'username':self.username2, 'password':self.password2})
        self.UserAuthorization2 = 'Bearer ' + response.data['access']
        response = self.client.post(self.login_url,{'username':self.username3, 'password':self.password3})
        self.UserAuthorization3 = 'Bearer ' + response.data['access']
        response = self.client.post(self.login_url,{'username':self.username4, 'password':self.password4})
        self.UserAuthorization4 = 'Bearer ' + response.data['access']

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

        # user 1 creates the concert
        response = self.client.post(
                 self.createConcertUrl,
                 json.dumps(info1),
                 content_type='application/json',
                 HTTP_AUTHORIZATION=self.UserAuthorization1
        )

        self.concert = Concert.objects.get(pk=response.data['concert_id'])

    def test_create_concert_report_empty_report_type(self):
        report_data = {
            'suggestion':'newsuggestion'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 400)


    def test_create_concert_report_invalid_report_type(self):
        report_data = {
            'report_type':'A',
            'suggestion':''
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )

        self.assertEqual(response.status_code, 400)

    def test_create_concert_report_name(self):
        report_data = {
            'report_type':'NAME',
            'suggestion':'Mahsar Fuat Ozkan Yilbasi Konseri'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'NAME')
        self.assertEqual(response.data['suggestion'],'Mahsar Fuat Ozkan Yilbasi Konseri')

    def test_create_concert_report_artist(self):
        report_data = {
            'report_type':'ARTIST',
            'suggestion':'{\"images\":[{\"height\":640,\"url\":\"https://i.scdn.co/image/db112ac3a4069660f697d400483d1b15dbb547f0\",\"width\":640},{\"height\":320,\"url\":\"https://i.scdn.co/image/28df9821ea9c020a5051b2596209d5dfd927fd24\",\"width\":320},{\"height\":160,\"url\":\"https://i.scdn.co/image/a0024a8d0dbe789a346fdbdb211884eef15fc20e\",\"width\":160}],\"spotify_id\":\"1MIVXf74SZHmTIp4V4paH4\",\"name\":\"Mabel\"}'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'ARTIST')
        self.assertEqual(response.data['suggestion'],'{\"images\":[{\"height\":640,\"url\":\"https://i.scdn.co/image/db112ac3a4069660f697d400483d1b15dbb547f0\",\"width\":640},{\"height\":320,\"url\":\"https://i.scdn.co/image/28df9821ea9c020a5051b2596209d5dfd927fd24\",\"width\":320},{\"height\":160,\"url\":\"https://i.scdn.co/image/a0024a8d0dbe789a346fdbdb211884eef15fc20e\",\"width\":160}],\"spotify_id\":\"1MIVXf74SZHmTIp4V4paH4\",\"name\":\"Mabel\"}')


    def test_create_concert_report_date_time(self):
        report_data = {
            'report_type':'DATE_TIME',
            'suggestion':'2018-01-01'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'DATE_TIME')
        self.assertEqual(response.data['suggestion'],'2018-01-01')

    def test_create_concert_report_description(self):
        report_data = {
            'report_type':'DESCRIPTION',
            'suggestion':'newdescription'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'DESCRIPTION')
        self.assertEqual(response.data['suggestion'],'newdescription')

    def test_create_concert_report_location(self):
        report_data = {
            'report_type':'LOCATION',
            'suggestion':'{\"venue\":\"los angeles nokia theatre\",\"coordinates\":\"34.044403 -118.267087\"}'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'LOCATION')
        self.assertEqual(response.data['suggestion'],'{\"venue\":\"los angeles nokia theatre\",\"coordinates\":\"34.044403 -118.267087\"}')

    def test_create_concert_report_min_price(self):
        report_data = {
            'report_type':'MIN_PRICE',
            'suggestion': 100
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'MIN_PRICE')
        self.assertEqual(int(response.data['suggestion']),100)

    def test_create_concert_report_max_price(self):
        report_data = {
            'report_type':'MAX_PRICE',
            'suggestion': 500
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'MAX_PRICE')
        self.assertEqual(int(response.data['suggestion']),500)

    def test_create_concert_report_seller_url(self):
        report_data = {
            'report_type':'SELLER_URL',
            'suggestion': 'http://www.biletix.com/etkinlik/UBH71/ANTALYA/tr'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'SELLER_URL')
        self.assertEqual(response.data['suggestion'],'http://www.biletix.com/etkinlik/UBH71/ANTALYA/tr')

    def test_create_concert_report_image(self):
        report_data = {
            'report_type':'IMAGE',
            'suggestion': 'https://www.google.com.tr/search?q=mfo+image&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj9qbu6prnYAhXI46QKHSWQCcAQ_AUICigB#imgrc=2Ypm92wPRhqUaM:'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_type'],'IMAGE')
        self.assertEqual(response.data['suggestion'],'https://www.google.com.tr/search?q=mfo+image&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj9qbu6prnYAhXI46QKHSWQCcAQ_AUICigB#imgrc=2Ypm92wPRhqUaM:')

    def test_upvote_own_concert_report(self):
        report_data = {
            'report_type':'ARTIST',
            'suggestion':'{\"images\":[{\"height\":640,\"url\":\"https://i.scdn.co/image/db112ac3a4069660f697d400483d1b15dbb547f0\",\"width\":640},{\"height\":320,\"url\":\"https://i.scdn.co/image/28df9821ea9c020a5051b2596209d5dfd927fd24\",\"width\":320},{\"height\":160,\"url\":\"https://i.scdn.co/image/a0024a8d0dbe789a346fdbdb211884eef15fc20e\",\"width\":160}],\"spotify_id\":\"1MIVXf74SZHmTIp4V4paH4\",\"name\":\"Mabel\"}'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )

        # concert report id is 1
        response = self.client.post('/concertreport/1/upvote/',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'You cannot upvote your own concert report.')

    def test_upvote_other_concert_report(self):
        report_data = {
            'report_type':'ARTIST',
            'suggestion':'{\"images\":[{\"height\":640,\"url\":\"https://i.scdn.co/image/db112ac3a4069660f697d400483d1b15dbb547f0\",\"width\":640},{\"height\":320,\"url\":\"https://i.scdn.co/image/28df9821ea9c020a5051b2596209d5dfd927fd24\",\"width\":320},{\"height\":160,\"url\":\"https://i.scdn.co/image/a0024a8d0dbe789a346fdbdb211884eef15fc20e\",\"width\":160}],\"spotify_id\":\"1MIVXf74SZHmTIp4V4paH4\",\"name\":\"Mabel\"}'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )
        concert_report = ConcertReport.objects.get(pk=response.data['concert_report_id'])
        # concert report id is 1
        response = self.client.post('/concertreport/1/upvote/',
                        HTTP_AUTHORIZATION = self.UserAuthorization2
                        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(concert_report.upvoters.all())),1)
        # try to upvote again
        # should not work.
        response = self.client.post('/concertreport/1/upvote/',
                        HTTP_AUTHORIZATION = self.UserAuthorization2
                        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'You have already upvoted this concert report.')


    def test_concert_report_upvote_threshold_reached(self):
        report_data = {
            'report_type':'DESCRIPTION',
            'suggestion':'newdesc'
        }

        response = self.client.post('/concert/1/report/',
                        json.dumps(report_data),
                        content_type='application/json',
                        HTTP_AUTHORIZATION = self.UserAuthorization1
                        )

        concert_report = ConcertReport.objects.get(pk=response.data['concert_report_id'])

        response = self.client.post('/concertreport/1/upvote/',
                        HTTP_AUTHORIZATION = self.UserAuthorization2
                        )
        response = self.client.post('/concertreport/1/upvote/',
                        HTTP_AUTHORIZATION = self.UserAuthorization3
                        )
        # Threshold is reached. It is 3.
        response = self.client.post('/concertreport/1/upvote/',
                        HTTP_AUTHORIZATION = self.UserAuthorization4
                        )
        concert = Concert.objects.get(pk=1)
        reporter = concert_report.reporter

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Since upvotes reached the limit, the related concert information has been changed and the associated report has been deleted.')
        # the concert should be updated.
        self.assertEqual(concert.description, 'newdesc')
        # the concert report should be deleted.
        self.assertEqual((concert_report in ConcertReport.objects.all()), False)
        # the reporter should gain a reliability point.
        self.assertEqual(reporter.reliability_points,1)
