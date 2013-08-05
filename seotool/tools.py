# -*- coding: utf-8 -*-
# Tools module.
# This module contains static helper functions.  They should receive all dependencies as parameters.
# You should not need classes in here. If you feel the need, consider adding a service class.
from datetime import datetime
from seotool import app
import dateutil.parser

def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)

    return validate


def is_expired(credentials):
    is_expired = True
    if credentials.get('token_expiry'):
        expire_date = datetime.strptime(credentials['token_expiry'], '%Y-%m-%dT%H:%M:%SZ')
        is_expired = expire_date < datetime.utcnow()

    return is_expired


@app.template_filter('time_fmt')
def time_fmt(value, format='%d.%m.%Y %H:%M'):
    tm = dateutil.parser.parse(value)
    dt = tm.astimezone(dateutil.tz.tzutc())
    ds = dt.strftime(format)
    return ds