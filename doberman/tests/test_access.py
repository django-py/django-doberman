import unittest
import string
import time

from doberman.utils.ip import AccessIPAddress
from doberman.utils.auth import AccessAttempt
from doberman.settings import *


try:
    from unittest import mock
except ImportError:
    import mock


class AccessAttemptTest(unittest.TestCase):

    def setUp(self):
        """Create a valid user for login
        """
        super(AccessAttemptTest, self).setUp()

        self.request = mock.MagicMock()
        self.response = mock.MagicMock()

        self.request.user.is_authenticated = mock.MagicMock()
        self.request_args = ['fake_arg']
        self.request_kwargs = {'fake': 'kwarg'}

        self.real_ip_address = '200.16.89.17'

    def _create_fake_response(self, **kwargs):
        if not kwargs:
            response = {'status_code': 200 }
        return response

    def _create_fake_meta_request(self, **kwargs):
        if not kwargs:
            meta_dict = {'REMOTE_ADDR': self.real_ip_address}
        return meta_dict

    def _create_fake_post(self, **kwargs):

        if not kwargs:
            post_data = {
                'username': 'user_name',
                'password': 'pass$$word'
            }
        return post_data

    def test_get_client_real_ip_address(self):

        self.request.META = {}
        access = AccessIPAddress()

        meta_dict = {
            'REMOTE_ADDR': self.real_ip_address
        }

        with mock.patch.dict(self.request.META, **meta_dict):
            client_ip_address = access.get_client_ip_address(self.request)
            self.assertEqual(client_ip_address, self.real_ip_address)

        with mock.patch.dict(self.request.META, HTTP_FORWARDED_FOR=self.real_ip_address):
            client_ip_address = access.get_client_ip_address(self.request)
            self.assertEqual(client_ip_address, self.real_ip_address)