#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains the main CUI script for the retrieval of data and the population of the reporting database
'''

import click

import import_data
import utils.console_output as cs

@click.group()
def recruitment_reporting():
    pass

@recruitment_reporting.command(help="Retrieves metics from Workable")
def get_workable_data():

    # Get all data from the Workable database
    cs.util_output("Retrieving data from the Workable API...")
    import_data.import_all_jobs()
    import_data.import_all_jobs_activities()
    import_data.import_all_candidates()
    import_data.import_all_account_members()
    cs.util_output("Data retrival process complete.")
    cs.util_output("Creating consolidated table...")
    import_data.create_consol_table()
    cs.util_output("Creation of consolidated table complete.")


if __name__ == '__main__':
    recruitment_reporting()
