import logging
import hashlib

from django.conf import settings
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out

from doberman.contrib.ipware import check_ipv4, check_ipv6, is_valid_ip
from doberman.exceptions import DobermanImproperlyConfigured

from .settings import DobermanSettings

logger = logging.getLogger(__name__)
# Doberman Settings
configuration = DobermanSettings()


def login_failed(**kwargs):
    """
    Login Failed
    """
    pass


def logged_in(**kwargs):
    """
    Logged in
    """
    pass


def logged_out(**kwargs):
    pass


class Doberman(object):
    """
    Doberman class
    """
    def __init__(self, request):
        """
        Doberman initialize...
        """

        self.request = request
        self.username = request.POST.get(configuration.username_form_field)
        self.configuration = configuration

        if self.username:
            self.user_hash = hashlib.md5(str(self.username)).hexdigest()  # Hash username
            user_login_failed.connect(login_failed, dispatch_uid=self.user_hash)

        else:
            # generate Doberman Exception..
            pass

        #user_logged_in.connect(self.login_failed, dispatch_uid='sadasdasd')
        #user_logged_out.connect(self.logged_out, dispatch_uid='asdasasdasdasdasd')

    def sniff(self):
        pass

    def get_user_ip(self, request):
        """
        get the client IP address bassed on a HTTPRequest
        """

        client_ip_address = None

        # searching the IP address
        for key in self.configuration.network.ip_meta_precedence_order:

            ip_meta_value = request.META.get(key, '').strip()

            if ip_meta_value != '':
                ips = [ip.strip().lower() for ip in ip_meta_value.split(',')]

                for ip_str in ips:

                    if ip_str and is_valid_ip(ip_str):

                        if not ip_str.startswith(self.configuration.network.non_public_ip_prefixes):
                            return ip_str

                        elif not self.configuration.network.real_ip_only:
                            loopback = ('127.0.0.1', '::1')

                            if client_ip_address is None:
                                client_ip_address = ip_str

                            elif client_ip_address in loopback and ip_str not in loopback:
                                client_ip_address = ip_str

        if client_ip_address is None and settings.DEBUG:
            raise DobermanImproperlyConfigured(
                "Unknown IP, maybe you are working on localhost/development, "
                "so please set in your setting: DOBERMAN_REAL_IP_ONLY=False"
            )

        return client_ip_address

