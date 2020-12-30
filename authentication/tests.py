from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase


class LoginTestCase(TestCase):
    BAD_REQUEST_RESPONSE = {
        '__all__': [
            'Please enter a correct username and password. Note that both fields may be case-sensitive.'
        ]
    }

    def test_login_data_validation(self):
        response = self.client.post('/auth/login/', {})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/json'))
        data = response.json()
        self.assertEqual(data, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
        })

    def test_login_with_unknown_credentials(self):
        credentials = {
            'username': 'alice',
            'password': 'ALICE123',
        }
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(username=credentials['username'])

        response = self.client.post('/auth/login/', credentials)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/json'))
        self.assertEqual(response.json(), self.BAD_REQUEST_RESPONSE)

    def test_inactive_user_cannot_login(self):
        credentials = {
            'username': 'bob',
            'password': 'BOB123',
        }
        get_user_model().objects.create_user(is_active=False, **credentials)

        response = self.client.post('/auth/login/', credentials)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json(), self.BAD_REQUEST_RESPONSE)

    def test_happy_path(self):
        credentials = {
            'username': 'john',
            'password': 'JOHN123',
        }
        get_user_model().objects.create_user(**credentials)

        response = self.client.post('/auth/login/', credentials)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn('sessionid', response.cookies)
        self.assertIn('Set-Cookie', response.cookies.output())
        self.assertRegexpMatches(response.cookies.output(), r'sessionid=[a-z0-9]+;')
        self.assertTrue(response.cookies['sessionid']['httponly'])

        response = self.client.delete('/auth/logout/')
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertIn('Set-Cookie', response.cookies.output())
        self.assertIn('sessionid=""', response.cookies.output())
