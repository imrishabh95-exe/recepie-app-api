from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    ''' test the user API public'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        '''test creating user with valid payload is successful'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name' : 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''testing creaintg user that already exist'''
        payload = {
            'email': 'test@gmail.com',
            'name' : 'Test Name',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''too short pasword'''
        payload = {
            'email': 'test@gmail.com',
            'name' : 'Test Name',
            'password': 'pww',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_toke_for_user(self):
        '''test that the token is ceated for user'''
        payload = {
            'email' : 'rishabh@gmail.com',
            'password': 'password123',
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        '''test taht toen is not created'''
        create_user(email='rishahbh@gmail.com', password='testpass')
        payload = {
            'email' : 'rishahbh@gmail.com',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''test not created user'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''test not created user'''
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        
