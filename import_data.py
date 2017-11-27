#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Imports and parses data from the Workable API for upload to the reporting database
'''

from sqlalchemy import desc

import customobjects.database_objects
import reference as r
import reference_private as rp
from customobjects.database_objects import TableJobs, TableActivities, TableCandidate
from customobjects.workable import Workable
import utils.console_output as cs
from utils.db_connect import mysql_db_sessionmaker
from utils.misc_functions import convert_string_to_datetime, convert_string_to_unicode


def get_all_job_shortcodes():
    ''' Retrieves the shortcodes (i.e. IDs) of all jobs held in the database

    :return:
    '''

    session = mysql_db_sessionmaker()
    all_codes = session.query(TableJobs.JobID).all()
    session.close()
    return all_codes

def get_last_activity_id(job_id):
    ''' Gets the last activity ID imported into the database for a given job ID

    :param job_id: ID of the Workable job to find the most recent activity for in the database
    :return:
    '''

    session = mysql_db_sessionmaker()
    qry = session.query(TableActivities.WorkableDateTime, TableActivities.ActivityID)\
        .filter(TableActivities.JobID==job_id).order_by(desc(TableActivities.WorkableDateTime))\
        .all()
    session.close()

    if qry:
        last_id = qry[0][1]
        return last_id
    else:
        return None

def get_last_job_id():
    ''' Gets the last activity ID imported into the database for a given job ID

    :param job_id: ID of the Workable job to find the most recent activity for in the database
    :return:
    '''

    session = mysql_db_sessionmaker()
    qry = session.query(TableJobs.ImportDateTime, TableActivities.JobID)\
        .order_by(desc(TableJobs.ImportDateTime))\
        .all()
    session.close()

    if qry:
        last_id = qry[0][1]
        return last_id
    else:
        return None

def get_last_candidate_id():
    ''' Gets the last candidate ID imported into the database

    :return:
    '''

    session = mysql_db_sessionmaker()
    qry = session.query(TableCandidate.WorkableDateTime, TableCandidate.CandidateID)\
        .order_by(desc(TableCandidate.WorkableDateTime))\
        .all()
    session.close()

    if qry:
        return qry[0][1]
    else:
        return None

def import_all_jobs():
    ''' Imports jobs data from Workable into the database

    :return:
    '''

    cs.util_output("Getting JOBS information from Workable API...")
    w = Workable(subdomain=rp.WORKABLE_SUBDOMAIN, private_key=rp.WORKABLE_PRIVATE_KEY)
    most_recent_job_id = get_last_job_id()

    jobs = w.get_jobs(since_id=most_recent_job_id)
    jobs_to_import = []

    # Populate database row objects for each job
    cs.util_output("Importing {} new jobs to the database...".format(len(jobs)))
    for job in jobs:

        row = customobjects.database_objects.TableJobs(
            ImportDateTime=convert_string_to_datetime(time_as_string=job['created_at']),
            JobID=job['shortcode'],
            JobDescription=job['title'],
            JobStatus=job['state']
        )
        jobs_to_import.append(row)

    # Add to the database
    session = mysql_db_sessionmaker()
    for row in jobs_to_import:
        if row.JobID!=most_recent_job_id:
            session.add(row)
    session.commit()
    session.close()
    cs.util_output("Jobs import process complete.")

def import_activities_for_job(job_id):
    ''' Imports the new activities for a given job ID since the last time the process was run

    :param job_id: Workable ID of the job to import activities for
    :return:
    '''

    w = Workable(subdomain=rp.WORKABLE_SUBDOMAIN, private_key=rp.WORKABLE_PRIVATE_KEY)

    most_recent_activity_id = get_last_activity_id(job_id=job_id)
    job_activities = w.get_jobs(id=job_id, activities=True, since_id=most_recent_activity_id)

    session = mysql_db_sessionmaker()

    if len(job_activities)>1:
        cs.util_output("Importing {} activities for job ID {}...".format(max(len(job_activities)-1,0),job_id))

    for activity in job_activities:

        row = customobjects.database_objects.TableActivities(
            ActivityID = activity['id'],
            CandidateID = activity['candidate']['id'] if 'candidate' in activity.keys() else None,
            JobID = job_id,
            StageID = None if activity['stage_name']==None else r.WORKABLE_STAGE_NAMES[activity['stage_name']],
            StageDesc = None if activity['stage_name'] == None else activity['stage_name'],
            MemberID = activity['member']['id'] if 'member' in activity.keys() else None,
            Body = convert_string_to_unicode(string_to_convert=activity['body']) if activity['body'] else None,
            DisqualifiedFlag = (activity['action']=='disqualified'),
            WorkableDateTime = convert_string_to_datetime(time_as_string=activity['created_at'])
        )
        # Workable since_id method seems to include that id in call
        if row.ActivityID!=most_recent_activity_id:
            session.add(row)

    session.commit()
    session.close()

def import_all_jobs_activities():
    ''' Import all activities for all jobs in the database

    :return:
    '''

    all_job_codes = get_all_job_shortcodes()

    for job_code in all_job_codes:
        import_activities_for_job(job_id=job_code[0])

def import_all_candidates():
    ''' Imports all candidates from the Workable database into the local database

    :return:
    '''

    cs.util_output("Getting CANDIDATE information from Workable API...")
    w = Workable(subdomain=rp.WORKABLE_SUBDOMAIN, private_key=rp.WORKABLE_PRIVATE_KEY)
    most_recent_candidate_id = get_last_candidate_id()

    candidates = w.get_candidates(since_id=most_recent_candidate_id)
    candidates_to_import = []

    # Populate database row objects for each job
    cs.util_output("Importing {} new candidates to the database...".format(len(candidates)))
    for candidate in candidates:

        row = customobjects.database_objects.TableCandidate(
            CandidateID = candidate['id'],
            CandidateName = convert_string_to_unicode(string_to_convert=candidate['name']),
            WorkableDateTime = convert_string_to_datetime(time_as_string=candidate['created_at']),
            SourceID = candidate['domain'] if candidate['domain'] else "Sourced",
            WorkableUrl = candidate['profile_url']
            )
        candidates_to_import.append(row)

    # Add to the database
    session = mysql_db_sessionmaker()
    for row in candidates_to_import:
        if row.CandidateID!=most_recent_candidate_id:
            session.add(row)

    session.commit()
    session.close()
    cs.util_output("Candidate import process complete.")
