[Development] django-doberman
===============

``django-doberman``   Django app that locks out users after too many failed login attempts. 


Requirements
------------
- Python => 2.7
- Django => 1.7


Installation
------------

1. Install python library using pip: pip install django-doberman

2. Add ``doberman`` to ``INSTALLED_APPS`` in your Django settings file

3. ./manage.py migrate doberman || or sync your database


Usage
-----

Add ``doberman.decorators.watch_login`` decorator to your login view. Example::


    class LoginView(FormView):
        template_name = 'example/login.html'
        form_class = AuthenticationForm

        @method_decorator(watch_login)
        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect(settings.LOGIN_REDIRECT_URL)
            return super(LoginView, self).dispatch(request, *args, **kwargs)

        def form_valid(self, form):
            user = form.get_user()
            login(self.request, user)
            return super(LoginView, self).form_valid(form)

        def get_success_url(self):
            return reverse('logged_in')


Settings
--------

DOBERMAN_MAX_FAILED_ATTEMPTS
    Number of max failed login attempt. Default: ``5``.

DOBERMAN_LOCKOUT_TIME
    Number of seconds after the failed login attempts are forgotten in seconds. Default: ``600``.

DOBERMAN_REAL_IP_ONLY

DOBERMAN_LOGIN_FORGOTTEN_SECONDS

DOBERMAN_USERNAME_FORM_FIELD

DOBERMAN_LOCKOUT_TEMPLATE

DOBERMAN_MODEL

DOBERMAN_IP_PRIVATE_IP_PREFIX

DOBERMAN_IP_META_PRECEDENCE_ORDER

Authors
-------

Library is by `Hanlle Nicolas Mendoza`.


.. Website: http://nicolasmendoza.org/
