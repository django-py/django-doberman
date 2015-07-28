# -*- coding: utf-8 -*-
"""
This is a adapted version of the util package called django-ipware created for @Val Neekman (thanks)
for more information, please see: https://github.com/un33k/django-ipware
"""
import socket
from ..settings import DOBERMAN_REAL_IP_ONLY, DOBERMAN_IP_META_PRECEDENCE_ORDER, DOBERMAN_NON_PUBLIC_IP_PREFIXES

from django.conf import settings

from ..exceptions import DobermanImproperlyConfigured


class AccessIPAddress(object):
    """
    Access IP addres
    Part of this code is based on package : https://github.com/un33k/django-ipware


    """
    def __init__(self):
        self.get_real_ip_only = DOBERMAN_REAL_IP_ONLY
        self.ip_meta_precedence_order = DOBERMAN_IP_META_PRECEDENCE_ORDER
        self.ip_non_public_ip_prefix = DOBERMAN_NON_PUBLIC_IP_PREFIXES

    @staticmethod
    def check_ipv6(ip_str):
        """
        Check is a valid IP V6
        """
        try:
            socket.inet_pton(socket.AF_INET6, ip_str)
        except socket.error:
            return False
        return True

    @staticmethod
    def check_ipv4(ip_str):
        """
        Check is a valid IP V4
        """
        try:
            socket.inet_pton(socket.AF_INET, ip_str)
        except AttributeError:
            try:
                socket.inet_aton(ip_str)
            except socket.error:
                return False
            return ip_str.count('.') == 3
        except socket.error:
            return False
        return True

    def is_valid_ip(self, ip_str):
        """
        Is valid IP
        """
        return self.check_ipv4(ip_str) or self.check_ipv6(ip_str)

    def get_client_ip_address(self, request):
        """
        get client IP address
        """

        client_ip_address = None

        # searching the IP address
        for key in self.ip_meta_precedence_order:

            ip_meta_value = request.META.get(key, '').strip()

            if ip_meta_value != '':
                ips = [ip.strip().lower() for ip in ip_meta_value.split(',')]

                for ip_str in ips:

                    if ip_str and self.is_valid_ip(ip_str):

                        if not ip_str.startswith(self.ip_non_public_ip_prefix):
                            return ip_str

                        elif not self.get_real_ip_only:
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