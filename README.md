# Workable KPI Reporting

## Overview

The purpose of this package is to retrieve data from the Workable API, to standardise the data to the house style and to insert into a reporting database.

## Prerequisites

The script requires:

1. A valid [**Workable**](https://developers.workable.com) account with an [API key generated](https://resources.workable.com/support/how-to-generate-an-api-access-token-for-workable)
2. A **Database backend** (the script has been tested with MySQL but should work with any database that [SqlAlchemy](https://www.sqlalchemy.org)supports)

## Configuration

The program requires a file called `reference_private.py` to be created in the top-level directory containing three variables:

1. `DB_CONNECTION_STRING` is the sqlalchemy connection string to your backend database (e.g. `DB_CONNECTION_STRING = "mysql://username:password@localhost/database-name"`)

2. `WORKABLE_PRIVATE_KEY` is the private API access key for Workable (see _Prerequisites_ above) (e.g. `DB_CONNECTION_STRING = 22a8a2f6f3740aebb0c676f1d798157c95011312905243a230cd05829716ec69`)

3. `WORKABLE_SUBDOMAIN` is the domain of your Workable instance (see _Prerequisites_ above) (e.g. `WORKABLE_SUBDOMAIN = "your-company-name"`)

## Command Line Interface

The management reporting tool uses a command line interface to control the import, processing and output of data from workable. The commands below are available for the `main.py` module.

Note also that the `--help` function works for all commands in the interface.

1. `get_workable_data`

Retrieves data from the Workable API, imports it into the database, standardises the data and then creates a consolidated table.
