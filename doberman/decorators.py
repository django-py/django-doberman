# -*- coding: utf-8 -*-
from functools import wraps

from lib.auth import AccessAttempt


def watch_login(func):
    """
    Decorator @watch_login
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_login(request, *args, **kwargs):

        response = func(request, *args, **kwargs)
        lockout = AccessAttempt(request)
        lockout.check_login()
        return response

    return decorated_login