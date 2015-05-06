from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import six


class AbstractCommonAccess(models.Model):
    """
    Common Access
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto=True)

    username = models.CharField(
        max_length=255,
        verbose_name=_("Username")
    )
    user_agent = models.CharField(
        max_length=255, blank=True,
        verbose_name=_("The client's user agent string")
    )

    path_info = models.CharField(
        max_length=255,
        verbose_name=_("A string representing the full path to the requested page, not including the domain.")
    )

    ip_address = models.IPAddressField(
        verbose_name=(_("The IP address of the client"))
    )

    using_https = models.BooleanField(
        default=False,
        verbose_name=_("True if the request was made with HTTPS.")
    )

    class Meta:
        abstract = True


class FailedAccessAttempt(AbstractCommonAccess):
    """
    Failed Access Attemps
    """
    params_post = models.TextField(verbose_name=_("GET data"))
    params_get = models.TextField(verbose_name=_("POST data"))
    is_locked = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __unicode__(self):
        return six.u('Attempted access: %s %s') % (self.username, self.ip_address)


class AccessLog(AbstractCommonAccess):
    """
    Access Log
    """
    logout_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return six.u('Access log for %s') % (self.username,)