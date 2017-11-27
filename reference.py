#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains constants and other references used by the script
'''

# Stage names used in the recruitment process are mapped to IDs in the tbl_DATA_stages table
WORKABLE_STAGE_NAMES = {'Applied':0,
                        'Sourced':0,
                        'Screening Interview': 1,
                        'Initial Screen': 1,
                        'Kite Interview': 1,
                        'Interview': 2,
                        'Stage 1 Interview': 2,
                        '1st Interview': 2,
                        'Hiring Manager': 2,
                        '2nd Interview': 3,
                        '2nd interview': 3,
                        'Manager Screen': 3,
                        'Stage 2 Interview': 3,
                        'Team Screen': 3,
                        'Technical Interview': 3,
                        'Additional Interview': 4,
                        'Additional Interviews': 4,
                        'CEO Interview': 4,
                        'Offer': 5,
                        'References': 6,
                        'Reference Checks': 6,
                        'Hired': 7}

# Database Tables

TBL_DATA_ACTIVITIES = "tbl_DATA_activities"

TBL_DATA_CANDIDATES = "tbl_DATA_candidates"
COL_CANDIDATES_ID = "CandidateID"

TBL_DATA_JOBS = "tbl_DATA_jobs"
COL_JOBS_ID = "JobID"

TBL_MASTER_STAGES = "tbl_MASTER_stages"

TBL_DATA_APPLICATIONS = "tbl_DATA_applications"