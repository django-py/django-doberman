# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FailedAccessAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=255, verbose_name='Username')),
                ('user_agent', models.CharField(max_length=255, verbose_name="The client's user agent string", blank=True)),
                ('ip_address', models.IPAddressField(verbose_name='The IP address of the client')),
                ('failed_attempts', models.PositiveIntegerField(default=0, verbose_name='Failed attempts')),
                ('is_locked', models.BooleanField(default=False)),
                ('is_expired', models.BooleanField(default=False)),
                ('params_post', models.TextField(verbose_name='GET data')),
                ('params_get', models.TextField(verbose_name='POST data')),
            ],
            options={
                'ordering': ('-created', 'username'),
                'abstract': False,
                'db_table': 'doberman_failed_access_attempt',
                'verbose_name': 'Failed access attempt',
                'verbose_name_plural': 'Failed access attempts',
            },
            bases=(models.Model,),
        ),
    ]
