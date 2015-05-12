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
    Default: ``10``.
    Number of max failed login attempt.

DOBERMAN_LOCKOUT_TIME
    Default: ``600`` (10 minutes).
    Number of seconds after the failed login attempts are forgotten in seconds.

DOBERMAN_REAL_IP_ONLY
    'Default': True
    Set to False if you are working on localhost or a development environment.

DOBERMAN_LOGIN_FORGOTTEN_SECONDS
    Default: ``300``
    Timeout forgotten login attempts of user.

DOBERMAN_USERNAME_FORM_FIELD
    Default: 'username'
    Field username form field, change when you are use a diferent "username", for example: 'email'.

DOBERMAN_LOCKOUT_TEMPLATE
    Path to alternative lockout template.

DOBERMAN_MODEL
    Allow define a different Model.


DOBERMAN_IP_META_PRECEDENCE_ORDER
    Default: (
    'HTTP_X_FORWARDED_FOR',
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
    )
    
    This used for discovery the real IP, you ca change the precedence order.


Authors
-------

Library is by `Hanlle Nicolas Mendoza`.


.. Website: http://nicolasmendoza.org/
