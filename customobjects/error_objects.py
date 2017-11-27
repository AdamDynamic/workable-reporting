#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains custom error classes used in the other modules to handle workflow
'''


class CustomError(AttributeError):
    '''
    Custom error description
    '''
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)