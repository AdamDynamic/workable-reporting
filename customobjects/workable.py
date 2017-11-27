#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains objects relating to the workable API
'''

import json

import utils.misc_functions as misc_functions


class Workable(object):

    def __init__(self, subdomain, private_key):

        self.api_url = "https://" + subdomain + ".workable.com/spi/v3/"
        self.api_headers = {'Authorization': 'Bearer' + ' ' + private_key}

    def _get_workable_api_request(self, tag, id=None, activities=False, created_after=None, since_id=None):
        '''

        :param tag: The tag to append to the end of the default API request string
        :param id: The id of the specific instance of the object type required (e.g. id of a specific candidate)
        :return: contents of the API call
        '''
        # ToDo: Add error handling for time-outs, wrong code, etc
        # ToDo: Add options for appending /:id to the call to return only specific candidate information
        # ToDo: Add check that submitted tag comes from a whitelist of approved tags
        # ToDo: Check is "activities" makes sense without "id" being specified (if not, raise error)

        # created_after must be UNIX or IDO8601 time
        if created_after:
            created_after = misc_functions.convert_datetime_to_unix(datetime_object=created_after)

        # Get the raw output from the API
        url = self.api_url + tag

        # Append modifiers to the url request
        if id:
            url += "/" + id
        if activities:
            url += "/activities"

        # 100 is the maximum limit (used to reduce number of calls to databse)
        url += '?limit=100'

        if since_id:
            url += '&since_id=' + since_id

        if created_after:
            url += "&created_after=" + str(created_after)

        output = []
        content = None
        # While loop to accommodate multiple pages being returned by the query
        # Pages are appended to the same result and returned as one
        while True:
            result = misc_functions.get_rate_limited_request(url=url, headers=self.api_headers)
            # Convert the raw string output into JSON format
            convert_to_json = json.loads(result.content)
            #pprint.pprint(convert_to_json)

            if activities:
                content = convert_to_json['activities']
            else:
                content = convert_to_json[tag]

            if output:
                output += content   # Only need to add the items, don't need the header
            else:
                output = content
            # If a new page is available, repeat the process.

            try:
                url = convert_to_json['paging']['next']
            except KeyError:
                break

        return output

    def get_jobs(self, id=None, activities=False, created_after=None, since_id=None):
        return self._get_workable_api_request(tag="jobs", id=id, activities=activities, created_after=created_after, since_id=since_id)

    def get_candidates(self, id=None, activities=False, since_id=None):
        return self._get_workable_api_request(tag="candidates", id=id, activities=activities, since_id=since_id)

    def get_events(self, id=None):
        return self._get_workable_api_request(tag="events", id=id)

    def get_subscriptions(self):
        return self._get_workable_api_request(tag="subscriptions")

    def get_members(self):
        return self._get_workable_api_request(tag="members")

    def get_recruiters(self):
        return self._get_workable_api_request(tag="recruiters")

    def get_stages(self):
        return self._get_workable_api_request(tag="stages")