# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=255, verbose_name='Username')),
                ('user_agent', models.CharField(max_length=255, verbose_name="The client's user agent string", blank=True)),
                ('path_info', models.CharField(max_length=255, verbose_name='A string representing the full path to the requested page, not including the domain.')),
                ('ip_address', models.IPAddressField(verbose_name='The IP address of the client')),
                ('using_https', models.BooleanField(default=False, verbose_name='True if the request was made with HTTPS.')),
                ('logout_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'doberman_access_log',
                'verbose_name': 'Access log',
                'verbose_name_plural': 'Access logs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FailedAccessAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=255, verbose_name='Username')),
                ('user_agent', models.CharField(max_length=255, verbose_name="The client's user agent string", blank=True)),
                ('path_info', models.CharField(max_length=255, verbose_name='A string representing the full path to the requested page, not including the domain.')),
                ('ip_address', models.IPAddressField(verbose_name='The IP address of the client')),
                ('using_https', models.BooleanField(default=False, verbose_name='True if the request was made with HTTPS.')),
                ('params_post', models.TextField(verbose_name='GET data')),
                ('params_get', models.TextField(verbose_name='POST data')),
                ('is_locked', models.BooleanField(default=False)),
                ('is_expired', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'doberman_failed_access_attempt',
                'verbose_name': 'Failed access attempt',
                'verbose_name_plural': 'Failed access attempts',
            },
            bases=(models.Model,),
        ),
    ]
