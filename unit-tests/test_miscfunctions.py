#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains unit tests for the utils.misc_functions.py module
'''

import unittest
import datetime

from utils import misc_functions

TEST_TIME_STRING = '2017-07-27T15:45:05.446Z'

class Test_MiscFunctions(unittest.TestCase):
    '''
    Unit tests for the utils.misc_functions module
    '''

    def test_datetime_parser_returns_datetime(self):
        ''' Tests that the object returned by the parser is a datetime object'''

        test_result = misc_functions.convert_string_to_datetime(time_as_string=TEST_TIME_STRING)
        self.assertIsInstance(test_result, datetime.datetime)

    def test_datetime_parser_returns_correct_date(self):
        ''' Tests whether the parser returns the date expected'''

        test_result = misc_functions.convert_string_to_datetime(TEST_TIME_STRING)
        expected_result = datetime.datetime(year=2017, month=7, day=27, hour=15, minute=45, second=5, microsecond=446, tzinfo=datetime.tzutc())
        self.assertEqual(test_result, expected_result)