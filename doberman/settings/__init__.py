# -*- coding: utf-8 -*-
from django.conf import settings
from .default import *
from .utils import setting_name


# Search for the real IP address
DOBERMAN_IP_META_PRECEDENCE_ORDER = getattr(
    settings,
    setting_name('IP-META-PRECEDENCE-ORDER'),
    DEFAULT_SETTING_IP_META_PRECEDENCE_ORDER
)

# Private IP addresses
DOBERMAN_PRIVATE_IP_PREFIXES = getattr(
    settings,
    setting_name('PRIVATE-IP-PREFIXES'),
    DEFAULT_SETTING_IP_PRIVATE_IP_PREFIX
)

DOBERMAN_NON_PUBLIC_IP_PREFIXES = DOBERMAN_PRIVATE_IP_PREFIXES + getattr(
    settings, setting_name('NON-PUBLIC-IP-PREFIXES'),
    DEFAULT_SETTING_IP_NON_PUBLIC_IP_PREFIX
)

DOBERMAN_REAL_IP_ONLY = getattr(
    settings,
    setting_name('REAL-IP-ONLY'),
    True
)

# Number of max failed login attempts
DOBERMAN_MAX_FAILED_ATTEMPTS = getattr(
    settings,
    setting_name('MAX-FAILED-ATTEMPTS'),
    10
)

# Number of seconds after the failed login attempts are forgotten in seconds (Default, 1 minute)
DOBERMAN_LOGIN_FORGOTTEN_SECONDS = getattr(
    settings,
    setting_name('LOGIN-FORGOTTEN-SECONDS'),
    60*5
)

DOBERMAN_USERNAME_FORM_FIELD = getattr(
    settings,
    setting_name('USERNAME-FORM-FIELD'),
    'username'
)

DOBERMAN_LOCKOUT_TIME = getattr(
    settings,
    setting_name('LOCKOUT-TIME'),
    60*10
)

DOBERMAN_IPLOCKOUT_TEMPLATE = getattr(
    settings,
    setting_name('IPLOCKOUT-TEMPLATE'),
    'doberman/ip_lockout.html'
)

DOBERMAN_CUSTOM_MODEL = getattr(
    settings,
    setting_name('MODEL'),
    False
)

# contrib.recaptcha library
DOBERMAN_RECAPTCHA_FORM_PROTECTION = getattr(
    settings,
    setting_name('RECAPTCHA-FORM-PROTECTION'),
    True
)

DOBERMAN_RECAPTCHA_KEY_SITE = getattr(
    settings,
    setting_name('RECAPTCHA-KEY-SITE'),
    None
)

DOBERMAN_RECAPTCHA_SECRET_KEY = getattr(
    settings,
    setting_name('RECAPTCHA-SECRET-KEY'),
    None
)

