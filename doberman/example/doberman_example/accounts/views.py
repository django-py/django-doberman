# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.views.generic import FormView
from django.utils.translation import gettext as _
from django.forms.utils import ErrorList
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from doberman.decorators import watch_login

from accounts.forms import *

User = get_user_model()


class LoginUserView(FormView):
    """
    Login User View
    @watch_logins
    """
    form_class = LoginUserForm
    template_name = 'accounts/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(watch_login)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginUserView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username'].lower()
        password = form.cleaned_data['password']


        user = User.objects.get(username=username)
        auth_user = authenticate(username=user.username, password=password)

        if auth_user:
            auth_login(self.request, auth_user)

        else:
            form._errors['username'] = ErrorList([_(u'Invalid username or password')])
            return self.form_invalid(form)

        return redirect('/')