# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from concert.models import Concert
from rest_framework.test import APITestCase
from rest_framework import status
from time import sleep
import json


class TestsForConcerts(APITestCase):
    #Populating Database
    def setUp(self):
        Concert.objects.create(artist="Duman", location="BogaziciUniTasoda", date="2017-05-20")
        sleep(1)
        Concert.objects.create(artist="Bulent Ortacgil", location ="BogaziciUniTasoda", date="2017-05-21")
        sleep(1)
                
    #Testcase 1
    def test_update_concert(self):

        url = '/concert/1/'
        data = {'artist': 'Sebnem Ferah', 'date':'2017-06-20', 'location':'BogaziciUniTasoda'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(json.loads(response.content), {'id': 1, 'artist': 'Sebnem Ferah', 'date':'2017-06-20', 'location':'BogaziciUniTasoda', 'minprice': 0, 'maxprice': 0})
    
    #Testcase 2
    def test_create_concert(self):
        url = '/concert/'
        data = {'artist': 'Sezen Aksu', 'date':'2017-05-20', 'location':'BogaziciUniTasoda'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {'id': 3, 'artist': 'Sezen Aksu', 'location': 'BogaziciUniTasoda', 'date': '2017-05-20', 'minprice': 0, 'maxprice': 0})

if __name__ == '__main__':
    unittest.main()
