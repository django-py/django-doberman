# -*- coding: utf-8 -*-
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

from django.db import models
from django.utils.translation import ugettext_lazy as _

from settings import DOBERMAN_LOGIN_FORGOTTEN_SECONDS


class AbstractFailedAccessAttempt(models.Model):
    """
    Abstract Failed Access Attempt
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name=_(u'Last attempt'))

    username = models.CharField(
        max_length=255,
        verbose_name=_("Username"),
    )
    user_agent = models.CharField(
        max_length=255, blank=True,
        verbose_name=_("The client's user agent string")
    )

    ip_address = models.IPAddressField(
        verbose_name=(_("The IP address of the client"))
    )

    failed_attempts = models.PositiveIntegerField(verbose_name=_(u'Failed login attempts'), default=0)
    is_locked = models.BooleanField(default=False, verbose_name=_(u'User/IP Locked'))
    is_expired = models.BooleanField(default=False, verbose_name=u'Lock expired')

    captcha_enabled = models.BooleanField(default=False, verbose_name=_("Captcha protection"))
    captcha_passed = models.BooleanField(default=False)
    captcha_attempts = models.SmallIntegerField(default=0, verbose_name=_("Captcha failed attempts"))

    class Meta:
        abstract = True
        ordering = ('-modified',)
        verbose_name = _("Access attempts")
        verbose_name_plural = _("Access attempts")

    def __str__(self):
        return self.username

    @classmethod
    def get_last_failed_access_attempt(cls, **kwargs):
        """
        Return Failed access attempt of Client
        :param ip_adress: String
        :return:
        """
        try:
            lockout = cls.objects.get(
                **kwargs
            )
        except cls.DoesNotExist:
            lockout = None

        if lockout:
            time_remaining = lockout.expiration_time
            if time_remaining and time_remaining <= 0:
                lockout.is_expired = True
                lockout.save()
                return None

        return lockout

    @property
    def expiration_time(self):
        """
        Returns the time until this access attempt is forgotten.
        """
        logging_forgotten_time = DOBERMAN_LOGIN_FORGOTTEN_SECONDS

        if logging_forgotten_time <= 0:
            return None

        now = timezone.now()
        delta = now - self.modified
        time_remaining = logging_forgotten_time - delta.seconds

        return time_remaining


class FailedAccessAttempt(AbstractFailedAccessAttempt):
    """
    Failed Access Attemps
    """
    params_post = models.TextField(verbose_name=_("GET data"))
    params_get = models.TextField(verbose_name=_("POST data"))