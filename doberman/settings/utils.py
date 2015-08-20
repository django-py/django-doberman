# -*- coding: utf-8 -*-
from .default import SETTING_PREFIX


def _to_setting_name(*names):
    """
    Humanize setting names
    :param names:
    :return:
    """
    return '_'.join([name.upper().replace('-', '_') for name in names if name])


def setting_name(*names):
    """
    Setting name..
    :param names:
    :return:
    """
    return _to_setting_name(*((SETTING_PREFIX,) + names))

