#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Functions for outputting data to the console
'''

import datetime

import click

def util_output(message):
    ''' Outputs to the console screen and logs as an INFO message via the logging module.

    :param message: The string to be displayed and logged
    :return:
    '''

    timestamp = datetime.datetime.now()
    enhanced_message = timestamp.strftime("%I:%M:%S") + ": " + str(message)
    click.echo(enhanced_message)