#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains miscellaneous functions used by other modules
'''

import datetime
from dateutil.parser import parse
import time
import requests

import unicodedata

def convert_string_to_datetime(time_as_string):
    ''' Converts strings to datetime object

    :param time_as_string: Format-agnostic string representation of a datetime
    :return:
    '''
    return parse(timestr=time_as_string)

def convert_datetime_to_unix(datetime_object):
    ''' Converts a python datetime object into the Unix representation of the time as a string

    :param datetime_object: Python datetime object
    :return: Unix time represented as string
    '''
    # Check if not datetime object
    assert isinstance(datetime_object, datetime.datetime)
    return time.mktime(datetime_object.timetuple())

def convert_string_to_unicode(string_to_convert):
    return unicodedata.normalize('NFKD', string_to_convert).encode('ascii', 'ignore')

# @Decorator function used to rate-limit API calls
def rate_limiter(max_calls_per_second):
    ''' Used with decorators to limit the number of calls to the Workable api

    From http://blog.gregburek.com/2011/12/05/Rate-limiting-with-decorators/

    :param max_calls_per_second: Maximum number of calls permitted per second
    :return: The decorated function
    '''
    min_interval = 1.0 / float(max_calls_per_second)

    def decorate(func):

        last_time_called = [0.0]

        def rate_limited_function(*args,**kargs):

            elapsed = time.clock() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait>0:
                time.sleep(left_to_wait)
            ret = func(*args,**kargs)
            last_time_called[0] = time.clock()

            return ret

        return rate_limited_function

    return decorate

@rate_limiter(max_calls_per_second=2)
def get_rate_limited_request(url, headers):
    result = requests.get(url, headers=headers)
    return result
