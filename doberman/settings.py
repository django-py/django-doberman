from django.conf import settings


def to_setting_name(*names):
    return '_'.join([name.upper().replace('-', '_') for name in names if name])


def setting_name(*names):
    return to_setting_name(*((SETTING_PREFIX,) + names))

DEFAULT_SETTING_IP_PRIVATE_IP_PREFIX = (
    '0.', '1.', '2.',  # externally non-routable
    '10.',  # class A private block
    '169.254.',  # link-local block
    '172.16.', '172.17.', '172.18.', '172.19.',
    '172.20.', '172.21.', '172.22.', '172.23.',
    '172.24.', '172.25.', '172.26.', '172.27.',
    '172.28.', '172.29.', '172.30.', '172.31.', # class B private blocks
    '192.0.2.',  # reserved for documentation and example code
    '192.168.',  # class C private block
    '255.255.255.',  # IPv4 broadcast address
    ) + (  # the following addresses MUST be in lowercase)
    '2001:db8:',  # reserved for documentation and example code
    'fc00:',  # IPv6 private block
    'fe80:',  # link-local unicast
    'ff00:',  # IPv6 multicast
    )


DEFAULT_SETTING_IP_META_PRECEDENCE_ORDER = (
    'HTTP_X_FORWARDED_FOR',  # X-Forwarded-For: client, proxy1, proxy2
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
    )

DEFAULT_SETTING_IP_NON_PUBLIC_IP_PREFIX = (
    '127.',  # IPv4 loopback device
    '::1',  # IPv6 loopback device
)


SETTING_PREFIX = 'DOBERMAN'

# Search for the real IP address in the following order
SETTING_IP_META_PRECEDENCE_ORDER = getattr(
    settings,
    setting_name('IP-META-PRECEDENCE-ORDER'),
    DEFAULT_SETTING_IP_META_PRECEDENCE_ORDER
)

# Private IP addresses
SETTING_PRIVATE_IP_PREFIXES = getattr(
    settings,
    setting_name('PRIVATE-IP-PREFIXES'),
    DEFAULT_SETTING_IP_PRIVATE_IP_PREFIX
)

SETTING_NON_PUBLIC_IP_PREFIXES = SETTING_PRIVATE_IP_PREFIXES + getattr(
    settings, setting_name('NON-PUBLIC-IP-PREFIXES'),
    DEFAULT_SETTING_IP_NON_PUBLIC_IP_PREFIX
)

SETTING_REAL_IP_ONLY = getattr(
    settings,
    setting_name('REAL-IP-ONLY'),
    True
)

# Number of max failed login attempts
SETTING_MAX_FAILED_ATTEMPTS = getattr(
    settings,
    setting_name('MAX-FAILED-ATTEMPTS'),
    10
)

# Number of seconds after the failed login attempts are forgotten in seconds (Default, 1 minute)
SETTING_LOGIN_FORGOTTEN_SECONDS = getattr(
    settings,
    setting_name('LOGIN-FORGOTTEN-SECONDS'),
    60*5
)

SETTING_USERNAME_FORM_FIELD = getattr(
    settings,
    setting_name('USERNAME-FORM-FIELD'),
    'username'
)

SETTING_LOCKOUT_TIME = getattr(
    settings,
    setting_name('LOCKOUT-TIME'),
    60*10
)

SETTING_LOCKOUT_TEMPLATE = getattr(
    settings,
    setting_name('SETTING-LOCKOUT-TEMPLATE'),
    'doberman/lockout.html'
)

SETTING_MODEL = getattr(
    settings,
    setting_name('MODEL'),
    False
)