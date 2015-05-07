# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..models import FailedAccessAttempt
from ..settings import SETTING_USERNAME_FORM_FIELD

from ..settings import (
    SETTING_MAX_FAILED_ATTEMPTS,
    SETTING_BLOCK_LOGIN_SECONDS,
    SETTING_LOCKOUT_TEMPLATE_NAME
)

from .ip import AccessIPAddress


class AccessAttempt(AccessIPAddress):
    """
    Failed Access Attempt class
    """

    def __init__(self, request, response, _class_model=None):
        self.request = request
        self.response = response

        self._class_model = FailedAccessAttempt if _class_model is None else _class_model

        self.ip = self.get_client_ip_address(self.request)

        self.username = self.request.POST.get(SETTING_USERNAME_FORM_FIELD, None)
        self.max_failed_attempts = SETTING_MAX_FAILED_ATTEMPTS
        self.block_login_seconds = SETTING_BLOCK_LOGIN_SECONDS
        self.template_name = SETTING_LOCKOUT_TEMPLATE_NAME

    def get_last_failed_access_attempt(self):
        """
        Return the last failed access attempt or None,
        the model can be change but is obligatory inplement the method "get_last_failed_access_attempt"
        """
        kwargs = {'ip_address': self.ip, 'username': self.username, 'is_expired': False}

        return self._model.get_last_failed_access_attempt(
            kwargs
        )

    def _check_failed_login(self):
        """
        'Private method', check failed logins
        """
        last_attempt = self.get_last_failed_access_attempt()

        if not last_attempt:
            # create a new entry
            user_access = self._models(ip_address=self.ip)

        if self.request.method == 'POST':

            if self.response.status_code != 302:

                user_access.user_agent = self.request.META.get('HTTP_USER_AGENT', '<unknown user agent>')[:255]
                user_access.username = self.username
                user_access.failed_attempts += 1
                user_access.params_get = self.request.GET
                user_access.params_post = self.request.POST

                if user_access.total_failed_attemps >= self.max_failed_attempts:
                    user_access.is_locked = True
                user_access.save()

            elif self.response.status_code == 302 and not user_access.is_locked:
                user_access.is_expired = True
                user_access.save()

        return user_access

    def check_login(self):
        """
        :return:
        """
        user_access = self._check_failed_login()

        if user_access.is_locked:
            return render_to_response(
                self.template_name, {
                    'user_access': user_access,
                    'lockout_time': self.block_login_seconds
                },
                context_instance=RequestContext(self.request)

            )