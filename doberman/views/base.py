from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from doberman import Doberman


class AccessAttemptView(View):
    """
    A generic login view with protection
    """
    def __init__(self, **kwargs):
        super(AccessAttemptView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            Doberman(request)

        return super(AccessAttemptView, self).dispatch(request, *args, **kwargs)