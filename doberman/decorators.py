# -*- coding: utf-8 -*-
from functools import wraps

from .utils.auth import AccessAttempt


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