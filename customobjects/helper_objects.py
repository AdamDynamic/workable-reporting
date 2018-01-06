#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains helper objects used in other modules
'''
from utils.misc_functions import convert_string_to_datetime


class Candidate(object):
    '''
    Helper object for Candidates retrieved from the Workable API
    '''

    def __init__(self):

        self.id = None
        self.name = None

    def __repr__(self):
        return "< Candidate Object: ID: {}, Name: {} >".format(self.id, self.name)


class Activity(object):
    '''
    Helper object for Actions retrieved from a Workable Jobs API request
    '''

    def __init__(self, workable_json):

        self.action = None
        self.body = None
        self.candidate = None
        self.timestamp = None
        self.id = None
        self.stage_name = None

        # Parse the Activity json object and populate the helper object
        self._parse_workable_json(workable_json=workable_json)

    def _parse_workable_json(self, workable_json):

        self.action = workable_json['action']
        self.body = workable_json['body']
        self.id = workable_json['id']

        self.candidate = Candidate()
        self.candidate.id = workable_json['candidate']['id']
        self.candidate.name = workable_json['candidate']['name']

        timestamp = workable_json['created_at']
        self.timestamp = convert_string_to_datetime(time_as_string=timestamp)

    def __repr__(self):
        return "< Action Object: Action: {}, Body: {}, Candidate: {}, TimeStamp: {}, ID: {}, StageName: {} >"\
            .format(self.action, self.body, self.candidate, self.timestamp, self.id, self.stage_name)

