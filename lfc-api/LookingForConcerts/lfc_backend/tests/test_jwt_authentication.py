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
class JSONWebTokenAuthTestCase(TestCase):

    def setUp(self):
        self.username = 'kemalberk'
        self.password = 'looking4C'
        self.email = 'kberk@gmail.com'
        self.credentials = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
        }
        self.update_profile = '/user/edit_profile'
        self.login_url = '/login/'
        self.signup_url = '/signup/'

        self.backend = authentication.JWTAuthentication()
        self.fake_token = 'ThisTokenIsFake'
        self.fake_header = 'Bearer ' + self.fake_token

        serializer = RegisteredUserSerializer(data=self.credentials)
        if serializer.is_valid():
            self.user = serializer.save()

        self.client = Client()

    def test_signup_valid_credentials(self):
        """
        Ensure that signup works with valid credentials
        """
        credentials = {
            'username': 'newuser',
            'password': 'helloworld',
            'email': 'helloworld@gmail.com',
        }
        response = self.client.post(
                 self.signup_url,
                 json.dumps(credentials),
                 content_type='application/json'
             )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], credentials['username'])


    def test_signup_invalid_credentials_duplicate_username(self):
        """
        Ensure that signup does not work with invalid credentials.
        """
        credentials = {
            'username': 'kemalberk',
            'password': 'helloworld',
            'email': 'helloworld@gmail.com',
        }
        response = self.client.post(
                 self.signup_url,
                 json.dumps(credentials),
                 content_type='application/json'
             )
        self.assertEqual(response.status_code, 400)

    def test_signup_invalid_credentials_duplicate_email(self):
        """
        Ensure that signup does not work with invalid credentials.
        """
        credentials = {
            'username': 'newuser',
            'password': 'helloworld',
            'email': 'kberk@gmail.com',
        }
        response = self.client.post(
                 self.signup_url,
                 json.dumps(credentials),
                 content_type='application/json'
             )
        self.assertEqual(response.status_code, 400)

    def test_jwt_login_valid_credentials(self):
        """
        Ensure that JWT login works with valid username and password
        """
        response = self.client.post(
            self.login_url,
            json.dumps(self.credentials),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200) # success
        self.assertFalse(response.data['access'] is None) # got an access token
        self.assertFalse(response.data['refresh'] is None) # got a refresh token

    def test_jwt_login_invalid_credentials(self):
        """
        Ensure that JWT login does not work with invalid username or password
        """
        invalid_credentials = {
            'username': self.username,
            'password': 'hacked'
        }
        response = self.client.post(
            self.login_url,
            json.dumps(invalid_credentials),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400) # fail

    def test_jwt_login_incomplete_credentials(self):
        """
        Ensure that JWT login does not work with incomplete username or password
        """
        incomplete_credentials = {
            'username': self.username
        }
        response = self.client.post(
            self.login_url,
            json.dumps(incomplete_credentials),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400) # fail

    def test_jwt_auth_valid_access_token(self):
        """
        Ensure that JWT auth works with valid access token
        """
        response = self.client.post(
            self.login_url,
            json.dumps(self.credentials),
            content_type='application/json'
        )
        token = response.data['access']
        auth_header = 'Bearer ' + token
        response = self.client.get(
            '/user/me/',
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_header
        )
        self.assertEqual(response.status_code, 200) # success

    def test_jwt_auth_fake_access_token(self):
        """
        Ensure that JWT auth does not work with fake access token
        """
        response = self.client.get(
            '/user/me/',
            content_type='application/json',
            HTTP_AUTHORIZATION=self.fake_header
        )
        self.assertEqual(response.status_code, 401) # unauthorized

    # def test_expired_token(self):
    #     print(str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']))
    #     old_access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    #     settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(seconds=0)
    #     print(str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']))
    #     response = self.client.post(
    #         self.login_url,
    #         json.dumps(self.credentials),
    #         content_type='application/json'
    #     )
    #
    #     access = AccessToken.for_user(self.user)
    #     access.set_exp(lifetime=timedelta(seconds=1))
    #     access['exp']=datetime.now()
    #
    #     print(access)
    #     print(str(access.lifetime))
    #
    #
    #     token = response.data['access']
    #     expired_auth_header = 'Bearer ' + token
    #     time.sleep(1)
    #     response = self.client.get(
    #         '/user/me/',
    #         content_type='application/json',
    #         HTTP_AUTHORIZATION=expired_auth_header
    #     )
    #
    #     # Restore settings
    #     try:
    #         settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = old_access_token_lifetime
    #     except KeyError:
    #         pass
    #
    #     #pprint.pprint(response.data)
