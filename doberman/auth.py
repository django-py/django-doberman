# -*- coding: utf-8 -*-
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.apps import apps

from .contrib.ipware import AccessIPAddress
from .exceptions import DobermanImproperlyConfigured
from .settings import (
    DOBERMAN_USERNAME_FORM_FIELD,
    DOBERMAN_MAX_FAILED_ATTEMPTS,
    DOBERMAN_LOCKOUT_TIME,
    DOBERMAN_IPLOCKOUT_TEMPLATE,
    DOBERMAN_CUSTOM_MODEL
)

def get_doberman_model():
        try:
            return apps.get_model(DOBERMAN_CUSTOM_MODEL)
        except ValueError:
            raise DobermanImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
        except LookupError:
            raise DobermanImproperlyConfigured(
                "DOBERMAN-MODEL refers to model '%s' that has not been installed: " % DOBERMAN_CUSTOM_MODEL
            )

class AccessAttempt(AccessIPAddress):
    """
    Failed Access Attempt class
    """
    max_failed_attempts = DOBERMAN_MAX_FAILED_ATTEMPTS
    block_login_seconds = DOBERMAN_LOCKOUT_TIME
    template_name = DOBERMAN_IPLOCKOUT_TEMPLATE

    def __init__(self, request, response):
        super(AccessAttempt, self).__init__()

        if isinstance(request, WSGIRequest):
            self.request = request
        else:
            self.request = request.request  #cbv

        self.response = response

        self.ip = self.get_client_ip_address(self.request)

        self.last_attempt_instance = None
        self.username = self.request.POST.get(DOBERMAN_USERNAME_FORM_FIELD, None)

        self._FailedAccessAttemptModel = get_doberman_model()  # doberman supported custom models, see documentation

    def get_last_failed_access_attempt(self, **kwargs):
        """
        Return the last failed access attempt or None,
        the model can be change but is obligatory implement the method "get_last_failed_access_attempt"
        """

        last_failed_access = self._FailedAccessAttemptModel.get_last_failed_access_attempt(
            **kwargs
        )

        return last_failed_access

    def check_failed_login(self):
        """
        'Private method', check failed logins, it's used for wath_login decorator
        """
        last_attempt = self.get_last_failed_access_attempt()

        if not last_attempt:
            # create a new entry
            user_access = self._FailedAccessAttemptModel(ip_address=self.ip)
        elif last_attempt:
            user_access = last_attempt

        if self.request.method == 'POST':
            if self.username is None:
                raise DobermanImproperlyConfigured(
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

    def inspect(self):
        """
        Inspect access attempt, used for catpcha flow
        :return:
        """
        last_attempt = self.get_last_failed_access_attempt(
            ip_address=self.ip,
            captcha_enabled=True,
            captcha_passed=False,
            is_expired=False
        )

        if last_attempt is None and not self.request.user.is_authenticated():
            # create a new entry
            user_access = self._FailedAccessAttemptModel(
                ip_address=self.ip,
                username=self.username,
                captcha_enabled=True,
                captcha_passed=False,
                is_expired=False
            )
        elif last_attempt:
            user_access = last_attempt

        if self.request.method == 'POST':

            if not self.request.user.is_authenticated():

                user_access.user_agent = self.request.META.get('HTTP_USER_AGENT', '<unknown user agent>')[:255]
                user_access.username = self.username
                user_access.failed_attempts += 1
                user_access.params_get = self.request.GET
                user_access.params_post = self.request.POST

                if user_access.failed_attempts >= self.max_failed_attempts:
                    user_access.is_locked = True
                user_access.save()

            elif self.request.user.is_authenticated() and last_attempt:
                last_attempt.is_expired = True
                last_attempt.save()

    def get_lockout_response(self):
        """
        :return:
        """

        return render_to_response(
            self.template_name,
            {'user_attempts': self.last_attempt_instance,
             'lockout_time': self.block_login_seconds,
             'ip_address': self.ip
             }, context_instance=RequestContext(self.request)
        )