import unittest
import string
import time
from doberman.utils.ip import AccessIPAddress

try:
    from unittest import mock
except ImportError:
    import mock


class AccessAttemptTest(unittest.TestCase):

    def setUp(self):
        """Create a valid user for login
        """
        super(AccessAttemptTest, self).setUp()

        self.request = 'fake request'
        self.request = mock.MagicMock()

        self.request.user.is_authenticated = mock.MagicMock()
        self.request_args = ['fake_arg']
        self.request_kwargs = {'fake': 'kwarg'}

        self.real_ip_address = '200.16.89.17 '

    def test_get_client_ip_address(self):
        self.request.META = {'REMOTE_ADDR', self.real_ip_address}
        client_ip_address = AccessIPAddress()
        self.assertEqual(client_ip_address, self.real_ip_address)