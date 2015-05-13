# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.apps import apps

from ..models import FailedAccessAttempt
from ..exceptions import DobermanImproperlyConfigured
from ..settings import SETTING_USERNAME_FORM_FIELD
from ..settings import (
    SETTING_MAX_FAILED_ATTEMPTS,
    SETTING_LOCKOUT_TIME,
    SETTING_LOCKOUT_TEMPLATE,
    SETTING_MODEL
)
from .ip import AccessIPAddress


class AccessAttempt(AccessIPAddress):
    """
    Failed Access Attempt class
    """
    model = FailedAccessAttempt
    max_failed_attempts = SETTING_MAX_FAILED_ATTEMPTS
    block_login_seconds = SETTING_LOCKOUT_TIME
    template_name = SETTING_LOCKOUT_TEMPLATE

    def __init__(self, request, response):
        super(AccessAttempt, self).__init__()
        self.request = request
        self.response = response
        self.ip = self.get_client_ip_address(self.request)
        self.last_attempt_instance = None
        self.username = self.request.POST.get(SETTING_USERNAME_FORM_FIELD, None)

        if SETTING_MODEL:
            try:
                self.model = apps.get_model(SETTING_MODEL)
            except LookupError:
                raise DobermanImproperlyConfigured(
                    "DOBERMAN-MODEL refers to model '%s' that has not been installed: " % SETTING_MODEL)

    def get_queryset(self, **kwargs):
        qs = self.model.get_last_failed_access_attempt(**kwargs)
        self.last_attempt_instance = qs

        return qs

    def get_last_failed_access_attempt(self):
        """
        Return the last failed access attempt or None,
        the model can be change but is obligatory inplement the method "get_last_failed_access_attempt"
        """
        kwargs = {'ip_address': self.ip, 'username': self.username, 'is_expired': False}

        return self.get_queryset(**kwargs)

    def check_failed_login(self):
        """
        'Private method', check failed logins
        """
        last_attempt = self.get_last_failed_access_attempt()

        if not last_attempt:
            # create a new entry
            user_access = self.model(ip_address=self.ip)
        elif last_attempt:
            user_access = last_attempt

        if self.request.method == 'POST':
            if self.username is None:
                raise DobermanSettingException(
                    "Bad username form field, if you are using a custom field please configure: "
                    "DOBERMAN_USERNAME_FORM_FIELD via settings."
                )

            if self.response.status_code != 302:

                user_access.user_agent = self.request.META.get('HTTP_USER_AGENT', '<unknown user agent>')[:255]
                user_access.username = self.username
                user_access.failed_attempts += 1
                user_access.params_get = self.request.GET
                user_access.params_post = self.request.POST

                if user_access.failed_attempts >= self.max_failed_attempts:
                    user_access.is_locked = True

                user_access.save()

            elif self.response.status_code == 302 and not user_access.is_locked:
                user_access.is_expired = True
                user_access.save()

        return user_access

    @property
    def is_ip_banned(self):
        """
        Ip banned
        :return:
        """
        kwargs = {'ip_address': self.ip, 'is_expired': False, 'is_locked': True}

        return self.get_queryset(**kwargs)

    def get_lockout_response(self):
        """
        :return:
        """

        return render_to_response(
            self.template_name,
            {'user_attempts': self.last_attempt_instance,
             'lockout_time': self.block_login_seconds
             }, context_instance=RequestContext(self.request)
        )