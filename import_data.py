#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Imports and parses data from the Workable API for upload to the reporting database
'''
from sqlalchemy import desc, or_

import customobjects.database_objects
import reference as r
import reference_private as rp
from customobjects.database_objects import TableJobs, TableActivities, TableCandidate, TableUsers, TableMetrics
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

    jobs = w.get_jobs()
    jobs_to_import = []

    # Populate database row objects for each job
    cs.util_output("Importing {} jobs to the database...".format(len(jobs)))
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
    session.query(TableJobs).delete()
    for row in jobs_to_import:
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

    #if len(job_activities)>1:
    cs.util_output("Importing {} activities for job ID {}...".format(max(len(job_activities)-1,0),job_id))

    for activity in job_activities:

        # Disqualified flag isn't captured in the "Stage Name"
        stage_id = None
        if activity['stage_name']:
            stage_id = r.WORKABLE_STAGE_NAMES[activity['stage_name']]
        elif activity['action']=='disqualified':
            stage_id = 99

        stage_desc = None
        if activity['stage_name']:
            stage_desc = activity['stage_name']
        elif activity['action']=='disqualified':
            stage_desc = activity['action']

        row = customobjects.database_objects.TableActivities(
            ActivityID = activity['id'],
            CandidateID = activity['candidate']['id'] if 'candidate' in activity.keys() else None,
            JobID = job_id,
            StageID = stage_id,
            StageDesc = stage_desc,
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

def get_first_activities_for_all_candidates():
    ''' Returns a dictionary indexed by CandidateID of the first Activity captured in the database for each candidate

    :return:
    '''

    session = mysql_db_sessionmaker()
    candidates = session.query(TableCandidate).all()
    activities = session.query(TableActivities).all()
    session.close()

    all_candidate_ids = list(set([cand.CandidateID for cand in candidates]))

    min_candidate_activity = {}

    for candidate_id in all_candidate_ids:

        candidate_activities = [row for row in activities if row.CandidateID == candidate_id]
        min_activity_row = None

        # ToDo: Find a more efficient way to do this
        # Find the row with the earliest timestamp
        for candidate_row in candidate_activities:
            if min_activity_row:
                if row.WorkableDateTime < min_activity_row.WorkableDateTime:
                    min_activity_row = candidate_row
            else:
                min_activity_row = candidate_row

        min_candidate_activity[candidate_id] = min_activity_row

    return min_candidate_activity

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

def import_all_account_members():
    ''' Retrieves the details of all users of the system

    :return:
    '''

    # ToDo: Need to capture account holders who are no longer active (e.g. RL?)

    w = Workable(subdomain=rp.WORKABLE_SUBDOMAIN, private_key=rp.WORKABLE_PRIVATE_KEY)
    members = w.get_members()
    recruiters = w.get_recruiters()

    all_users = members + recruiters
    session = mysql_db_sessionmaker()

    session.query(TableUsers).delete()

    for user in all_users:

        row =  TableUsers(
            UserID = user['id'],
            UserName = user['name'],
            UserEmail = user['email'],
            IsRecruiter = ('clearmatics' not in user['email'])
        )
        session.add(row)

    session.commit()
    session.close()

def create_consol_table():
    ''' Creates a consolidated table for use with KPI analysis

    :return:
    '''

    session = mysql_db_sessionmaker()

    activities = session.query(TableActivities).all()

    # Get all users and create a dictionary of whether they are recruiters or not
    users = session.query(TableUsers).all()
    users_dict = {user.UserID:user.IsRecruiter for user in users}

    # Get all candidates
    candidates = session.query(TableCandidate).all()

    # Get the minimum candidate activity for each candidate
    min_candidate_activities = get_first_activities_for_all_candidates()

    # ToDo: Need to include a check that the same stage isn't repeated for the same candidate?

    # For each candidate in the database, get all activities that relate to a change in state for that candidate
    for candidate in candidates:

        min_activity_row = min_candidate_activities[candidate.CandidateID]
        assert min_activity_row is not None, "No activities found for candidate {} (try re-importing activities)"\
            .format(candidate.CandidateID)

        min_activity_time = min_activity_row.WorkableDateTime
        candidate_activities = [act for act in activities if act.CandidateID == candidate.CandidateID]

        # ToDo: Re-write this section
        # Check that the minimum activity is unique and then unpack
        min_candidate_activity = [act for act in candidate_activities if act.WorkableDateTime == min_activity_time]
        if len(min_candidate_activity) > 1:
            all_user_ids = [row.MemberID for row in min_candidate_activity]
            if len(list(set(all_user_ids))) == 1:                       # i.e. If the same user for every row
                min_candidate_activity = min_candidate_activity[0]      # then unpack from the list
            else:
                raise
        else:
            min_candidate_activity = min_candidate_activity[0]


        # Create the first row for the candidate
        min_row = TableMetrics(
                    CandidateID=min_candidate_activity.CandidateID,
                    JobID=min_candidate_activity.JobID,
                    ActivityID=min_candidate_activity.ActivityID,
                    StageID=0,
                    StageDesc=None,
                    ActivityTimeStamp=min_candidate_activity.WorkableDateTime,
                    DisqualifiedFlag=min_candidate_activity.DisqualifiedFlag,
                    SourceID=None,
                )
        # Set the Sourced properties for all rows
        source_id = 'Unknown'
        if min_candidate_activity.MemberID in users_dict.keys():
            if users_dict[min_candidate_activity.MemberID] == 1:
                source_id = "Agent"
                min_row.StageDesc = "Sourced"
            else:
                source_id = candidate.SourceID
                min_row.StageDesc = "Applied"
        else:
            min_row.StageDesc = "Applied"
            source_id = candidate.SourceID

        min_row.SourceID = source_id
        session.add(min_row)

        for activity in candidate_activities:

            # The first row has already been created so doesn't need to be created again
            if activity.WorkableDateTime != min_activity_time:
                # If an activity is explicitly described, import the data
                if (activity.StageDesc is not None) or (activity.DisqualifiedFlag == True):
                    # Add row to the session directly
                    row = TableMetrics(
                        CandidateID=activity.CandidateID,
                        JobID=activity.JobID,
                        ActivityID=activity.ActivityID,
                        StageID=activity.StageID,
                        StageDesc=activity.StageDesc,
                        ActivityTimeStamp=activity.WorkableDateTime,
                        DisqualifiedFlag=activity.DisqualifiedFlag,
                        SourceID=source_id,
                    )
                    session.add(row)

    # Clear old data out of the table
    session.query(TableMetrics).delete()

    session.commit()
    session.close()