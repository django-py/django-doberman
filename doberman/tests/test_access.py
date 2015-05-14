import random

from django.test import TestCase

from doberman.utils.auth import AccessAttempt
from doberman.settings import SETTING_USERNAME_FORM_FIELD

from django.http import HttpRequest, HttpResponse


class AccessAttemptTest(TestCase):

    def setUp(self):
        """Create a valid user for login
        """
        super(AccessAttemptTest, self).setUp()
        self.setting_username_form_field = SETTING_USERNAME_FORM_FIELD
        self.invalid_username = 'invalid_username'
        self.random_password = random.randrange(01111110, 99910599, 8)
        self.real_ip = '200.16.89.17'

    def _login(self, username, password):
        response = self.client.post('/login/', {'username': username, 'password': password})
        return response

    def http_request(self):
        request = HttpRequest()
        request.COOKIES = {}
        request.path = '/login/'
        request.method = 'POST'
        request.META = {
            'PATH_INFO': request.path,
            'SERVER_NAME': u'test_server',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'REQUEST_METHOD': request.method,
            'REMOTE_ADDR': self.real_ip

        }
        request.POST = {
            self.setting_username_form_field: self.invalid_username,
            'password': self.random_password
        }

        return request

    def http_response(self):
        response = HttpResponse()
        response.status_code = 200
        return response

    def _access_attempt(self, request, response):
        access_attempt = AccessAttempt(request, response)
        return access_attempt

    def test_get_last_failed_access_attempt(self):
        """
        request / factory
        :return:
        """

        request = self.http_request()
        response = self.http_response()

        response.status_code = 200

        access = self._access_attempt(request, response)

        access.get_last_failed_access_attempt()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(access.username)

    def test_check_failed_login(self):
        lockout = self._access_attempt(self.http_request(), self.http_response())
        user_access = lockout.check_failed_login()

        self.assertFalse(user_access.is_locked)
        self.assertFalse(lockout.is_ip_banned)
        self.assertEqual(self.real_ip, lockout.ip)

