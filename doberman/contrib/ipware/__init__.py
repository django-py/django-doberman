# -*- coding: utf-8 -*-
"""
This is a adapted version of the util package called django-ipware created for @Val Neekman (thanks)
for more information, please see: https://github.com/un33k/django-ipware
"""
import socket
from django.conf import settings
from doberman import configuration

from doberman.exceptions import DobermanImproperlyConfigured


# class IPWare(object):
#     """
#     Access IP addres
#     Part of this code is based on package : https://github.com/un33k/django-ipware
#     """
#     # def __init__(self):
#     #     self.get_real_ip_only = configuration.network.real_ip_only
#     #     self.ip_meta_precedence_order = configuration.network.ip_meta_precedence_order
#     #     self.ip_non_public_ip_prefix = configuration.network.non_public_ip_prefixes


def check_ipv6(ip_str):
    """
    Return True if is a valid IP v6
    """

    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
    except socket.error:
        return False
    return True


def check_ipv4(ip_str):
    """
    Return True if is a valid IP v4
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
    return True if is a valid IP v4 or IP v6.
    """
    return check_ipv4(ip_str) or check_ipv6(ip_str)


