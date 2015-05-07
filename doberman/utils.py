import socket

from .settings import SETTING_PREFIX

from .settings import (
    SETTING_IP_META_PRECEDENCE_ORDER,
    SETTING_IP_NON_PUBLIC_IP_PREFIX,
    SETTING_GET_REAL_IP_ONLY
)

__all__ = ['setting_name', 'get_ip']


def to_setting_name(*names):
    return '_'.join([name.upper().replace('-', '_') for name in names if name])


def setting_name(*names):
    return to_setting_name(*((SETTING_PREFIX,) + names))


def check_ipv4(ip_str):
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


def check_ipv6(ip_str):
    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
    except socket.error:
        return False
    return True


def is_valid_ip(ip_str):
    return check_ipv4(ip_str) or check_ipv6(ip_str)


def get_client_ip(request):

    client_ip_address = None

    real_ip_only = SETTING_GET_REAL_IP_ONLY

    # searching the IP address
    for key in SETTING_IP_META_PRECEDENCE_ORDER:
        ip_meta_value = request.META.get(key, '').strip()

        if ip_meta_value != '':
            ips = [ip.strip().lower() for ip in ip_meta_value.split(',')]

            for ip_str in ips:

                if ip_str and is_valid_ip(ip_str):

                    if not ip_str.startswith(SETTING_IP_NON_PUBLIC_IP_PREFIX):
                        return ip_str

                    elif not real_ip_only:
                        loopback = ('127.0.0.1', '::1')

                        if client_ip_address is None:
                            client_ip_address = ip_str

                        elif client_ip_address in loopback and ip_str not in loopback:
                            client_ip_address = ip_str

    return client_ip_address