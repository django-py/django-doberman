# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import PasswordInput, Input
from django.contrib.auth import get_user_model

from django import forms

user = get_user_model()


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = Input(
            attrs={
                'class': 'form-control',
                'placeholder': _(u'Username')
            }
        )
        self.fields['password'].widget = PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _(u'Password')
            }
        )

    def clean_username(self):

        if self.data['username']:
            username = self.data['username'].lower()
            try:
                user.objects.get(username=username)
            except user.DoesNotExist:
                raise forms.ValidationError(_(u'Invalid username or password'))

        return self.data['username']

    def clean(self, *args, **kwargs):
        self.clean_username()
        return super(LoginUserForm, self).clean(*args, **kwargs)