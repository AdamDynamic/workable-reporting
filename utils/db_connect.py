#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains functions relating to the connection to the database
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import reference_private as rp

# Create mysql database sessionmakers
_mysql_engine = create_engine(rp.DB_CONNECTION_STRING)
_mysql_base = declarative_base()
_mysql_base.metadata.bind = _mysql_engine

mysql_db_sessionmaker = scoped_session(sessionmaker(bind=_mysql_engine, autoflush=False))