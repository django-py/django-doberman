import os
import sys
import socket

from django import forms
from django.conf import settings
try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import HiddenInput

from captcha import client
from captcha.widgets import ReCaptcha

from doberman.settings import DOBERMAN_USERNAME_FORM_FIELD
from doberman.auth import get_doberman_model
from doberman.contrib.ipware import AccessIPAddress
from doberman.models import FailedAccessAttempt


class DobermanCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _('Incorrect, please try again.'),
        'captcha_error': _('Error verifying input, please try again.'),
    }

    def __init__(self, public_key=None, private_key=None, use_ssl=None,
                 attrs={}, *args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of
        attributes to be passed to the ReCaptcha widget class. The widget will
        loop over any options added and create the RecaptchaOptions
        JavaScript variables as specified in
        https://code.google.com/apis/recaptcha/docs/customization.html
        """

        self.attrs = attrs
        self.public_key = public_key if public_key else \
            settings.RECAPTCHA_PUBLIC_KEY
        self.private_key = private_key if private_key else \
            settings.RECAPTCHA_PRIVATE_KEY
        self.use_ssl = use_ssl if use_ssl is not None else getattr(
            settings, 'RECAPTCHA_USE_SSL', False)

        self.widget = HiddenInput()
        self.blocked = False
        super(DobermanCaptchaField, self).__init__(*args, **kwargs)

        self.doberman_model = get_doberman_model()
        self._username = None
        self._ip = None
        self._last_attempt = None
        self.required = True

    def _captcha_form(self):
        """
        captcha form
        :return:
        """
        try:
            last_attempt = FailedAccessAttempt.objects.get(
                ip_address=self._ip,
                is_locked=True,
                captcha_enabled=True,
                is_expired=False

            )
        except FailedAccessAttempt.DoesNotExist:
            last_attempt = None
            self.required = False
            self.widget = HiddenInput()

        if last_attempt:
            self._last_attempt = last_attempt

            if last_attempt.is_locked:
                self.required = True
                self.widget = ReCaptcha(
                    public_key=self.public_key, use_ssl=self.use_ssl, attrs=self.attrs
                )

    def dynamic_fields(self):
        f = sys._getframe()
        while f:
            if 'request' in f.f_locals:
                request = f.f_locals['request']
                if request:
                    self._username = request.POST.get(DOBERMAN_USERNAME_FORM_FIELD, None)
                    access = AccessIPAddress()
                    self._ip = access.get_client_ip_address(request)

                    return self._ip
            f = f.f_back

    def initialize(self):
        self.dynamic_fields()
        self._captcha_form()

    def clean(self, values):
        if self.required:
            super(DobermanCaptchaField, self).clean(values[1])
            recaptcha_challenge_value = smart_unicode(values[0])
            recaptcha_response_value = smart_unicode(values[1])
            if os.environ.get('RECAPTCHA_TESTING', None) == 'True' and \
                    recaptcha_response_value == 'PASSED':
                return values[0]

            try:
                check_captcha = client.submit(
                    recaptcha_challenge_value,
                    recaptcha_response_value, private_key=self.private_key,
                    remoteip=self._ip, use_ssl=self.use_ssl)

            except socket.error: # Catch timeouts, etc
                raise ValidationError(
                    self.error_messages['captcha_error']
                )

            if not check_captcha.is_valid:
                self._last_attempt.captcha_attempts += 1
                self._last_attempt.save()
                raise ValidationError(
                    self.error_messages['captcha_invalid']
                )
            return values[0]
