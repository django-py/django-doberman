# -*- coding: utf-8 -*-
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import six

from .settings import SETTING_LOGIN_FORGOTTEN_SECONDS


class AbstractFailedAccessAttempt(models.Model):
    """
    Abstract Failed Access Attempt
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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

    failed_attempts = models.PositiveIntegerField(verbose_name=_(u'Failed attempts'), default=0)
    is_locked = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ('-created', 'username')
        db_table = 'doberman_failed_access_attempt'
        verbose_name = _("Failed access attempt")
        verbose_name_plural = _("Failed access attempts")

    def __unicode__(self):
        return six.u('Attempted access: %s %s') % (self.username, self.ip_address)

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
        logging_forgotten_time = SETTING_LOGIN_FORGOTTEN_SECONDS

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