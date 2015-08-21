# -*- coding: utf-8 -*-
from django.conf import settings
from .default import *
from .utils import setting_name


class BehaviorSettings(object):
    def __init__(self):
        self.lockout_time = getattr(settings, setting_name('LOCKOUT-TIME'), 60*10)
        self.max_failed_attempts = getattr(settings, setting_name('MAX-FAILED-ATTEMPTS'), 10)
        # Number of seconds after the failed login attempts are forgotten in seconds (Default, 1 minute)
        self.login_forgotten_seconds = getattr(settings, setting_name('LOGIN-FORGOTTEN-SECONDS'), 60*5)
        self.captcha_form_protection = getattr(settings, setting_name('RECAPTCHA-FORM-PROTECTION'), True)


class NetworkSettings(object):
    def __init__(self):
        # Search for the real IP address
        self.ip_meta_precedence_order = getattr(
            settings, setting_name('IP-META-PRECEDENCE-ORDER'),
            DEFAULT_SETTING_IP_META_PRECEDENCE_ORDER
        )
        # Private IP addresses
        self.private_ip_prefixes = getattr(
            settings,
            setting_name('PRIVATE-IP-PREFIXES'),
            DEFAULT_SETTING_IP_PRIVATE_IP_PREFIX
        )
        self.non_public_ip_prefixes = self.private_ip_prefixes + getattr(
            settings,
            setting_name('NON-PUBLIC-IP-PREFIXES'), DEFAULT_SETTING_IP_NON_PUBLIC_IP_PREFIX)

        self.real_ip_only = getattr(settings, setting_name('REAL-IP-ONLY'), True)


class CaptchaSettings(object):
    def __init__(self):
        self.secret_key = getattr(settings,setting_name('RECAPTCHA-SECRET-KEY'), None)
        self.key_site = getattr(settings, setting_name('RECAPTCHA-KEY-SITE'), None)


class DobermanSettings(object):
    def __init__(self):
        self.username_form_field = getattr(settings, setting_name('USERNAME-FORM-FIELD'), 'username')
        self.doberman_model = getattr(settings, setting_name('MODEL'), False)
        self.iplockout_template = getattr(settings, setting_name('IPLOCKOUT-TEMPLATE'), 'doberman/ip_lockout.html')

        self.captcha = CaptchaSettings()
        self.network = NetworkSettings()
        self.behavior = BehaviorSettings()

    def __del__(self):
            print "DobermanSettings: bye"