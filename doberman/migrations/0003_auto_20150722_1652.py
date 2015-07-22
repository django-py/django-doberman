# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doberman', '0002_auto_20150721_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='failedaccessattempt',
            options={'ordering': ('-modified',), 'verbose_name': 'Access attempts', 'verbose_name_plural': 'Access attempts'},
        ),
        migrations.AlterField(
            model_name='failedaccessattempt',
            name='captcha_attempts',
            field=models.SmallIntegerField(default=0, verbose_name='Captcha failed attempts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='failedaccessattempt',
            name='captcha_enabled',
            field=models.BooleanField(default=False, verbose_name='Captcha protection'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='failedaccessattempt',
            name='failed_attempts',
            field=models.PositiveIntegerField(default=0, verbose_name='Failed login attempts'),
            preserve_default=True,
        ),
        migrations.AlterModelTable(
            name='failedaccessattempt',
            table=None,
        ),
    ]
