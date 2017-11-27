#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains the database table objects created to support the SQLAlchemy ORM mappings. Each table in the primary
database is represented by a mapping object here.
'''

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

import reference as r

Base = declarative_base()

class TableActivities(Base):
    '''
    SQLAlchemt ORM class for the tbl_DATA_activities table
    '''

    __tablename__ = r.TBL_DATA_ACTIVITIES

    ID = Column(Integer, primary_key=True)
    ImportDateTime = Column(DateTime)
    ActivityID = Column(String)
    CandidateID = Column(String, ForeignKey(r.TBL_DATA_CANDIDATES + "." + r.COL_CANDIDATES_ID), nullable=True)
    JobID = Column(String, ForeignKey(r.TBL_DATA_JOBS + "." + r.COL_JOBS_ID))
    StageID = Column(String, nullable=True)
    StageDesc = Column(String, nullable=True)
    MemberID = Column(String)
    Body = Column(String, nullable=True)
    DisqualifiedFlag = Column(String)
    WorkableDateTime = Column(DateTime)

    def __repr__(self):
        return "<{}: " \
               "ID: {}, " \
               "ImportDateTime: {}, " \
               "ActivityID: {}, " \
               "CandID: {}, " \
               "JobID: {}, " \
               "StageID: {}, " \
               "StageDesc: {}, " \
               "MemberID: {}, "\
               "Body: {}, " \
               "DisqFlag: {} " \
               "ImportDateTime: {} >"\
            .format(self.__tablename__,
                    self.ID,
                    self.ImportDateTime,
                    self.ActivityID,
                    self.CandidateID,
                    self.JobID,
                    self.StageID,
                    self.StageDesc,
                    self.Body,
                    self.DisqualifiedFlag,
                    self.WorkableDateTime)


class TableCandidate(Base):
    '''
    SQLAlchemy ORM class for the tbl_DATA_candidates table
    '''

    __tablename__ = r.TBL_DATA_CANDIDATES

    ID = Column(Integer, primary_key=True)
    CandidateID = Column(String)
    CandidateName = Column(String)
    WorkableDateTime = Column(DateTime)
    SourceID = Column(String)
    WorkableUrl = Column(String)

    def __repr__(self):
        return "< {}: " \
               "ID: {}, " \
               "CandID: {}, " \
               "CandName: {}, " \
               "WorkableDateTime: {}, " \
               "SourceID: {}, " \
               "WorkableURL: {} >"\
            .format(self.__tablename__,
                    self.ID,
                    self.CandidateID,
                    self.CandidateName,
                    self.WorkableDateTime,
                    self.SourceID,
                    self.WorkableUrl)


class TableJobs(Base):
    '''
    SQLAlchemy class for the tbl_DATA_jobs table
    '''

    __tablename__ = r.TBL_DATA_JOBS

    ID = Column(Integer, primary_key=True)
    ImportDateTime = Column(DateTime)
    JobID = Column(String)
    JobDescription = Column(String)
    JobStatus = Column(Integer)
    LastUpdated = Column(DateTime)

    def __repr__(self):
        return "< {}: " \
               "ID: {}, " \
               "ImportDateTime: {}, " \
               "JobID: {}, " \
               "JobDesc: {}, " \
               "JobStatus: {}, " \
               "LastUpdated: {} >"\
            .format(self.__tablename__,
                    self.ID,
                    self.ImportDateTime,
                    self.JobID,
                    self.JobDescription,
                    self.JobStatus,
                    self.LastUpdated)
