# -*- coding: utf-8 -*-
import logging
from functools import wraps

from .core import AccessAttempt

logger = logging.getLogger(__name__)

def watch_login(func):
    """
    Decorator @watch_login
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_login(request, *args, **kwargs):

        response = func(request, *args, **kwargs)

        lockout = AccessAttempt(request, response)
        user_access = lockout.check_failed_login()

        if user_access.is_locked or lockout.is_ip_banned:
            return lockout.get_lockout_response()

        return response

    return decorated_login


def protect_login_with_captcha(func):
    """
    Protect the login with a captcha after of N failed access attempts
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_login(request, *args, **kwargs):
        response = func(request, *args, **kwargs)

        access_attempt = AccessAttempt(request, response)
        access_attempt.inspect()

        return response

    return decorated_login