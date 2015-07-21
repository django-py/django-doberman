# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doberman', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='failedaccessattempt',
            name='captcha_attempts',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='failedaccessattempt',
            name='captcha_enabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='failedaccessattempt',
            name='captcha_passed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='failedaccessattempt',
            name='is_expired',
            field=models.BooleanField(default=False, verbose_name='Lock expired'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='failedaccessattempt',
            name='is_locked',
            field=models.BooleanField(default=False, verbose_name='User/IP Locked'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='failedaccessattempt',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Last attempt'),
            preserve_default=True,
        ),
    ]
