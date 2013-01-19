#!/usr/bin/env python

import argparse
import json
import os

from time import localtime
from time import strftime

import kipptbackup
from kipptbackup.config import *


def backup():
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--username", help="""
        Kippt username.
        """)
    parser.add_argument("-T", "--token", help="""
        Kippt API token.
        """)
    parser.add_argument("-l", "--location", help="""
        location where the dump files will be stored.
        """)
    parser.add_argument("-p", "--prefix", help="""
        time prefix format to prepend dump file names with.
        """)
    parser.add_argument("--no-prefix", help="""
        to not prepend dump files with any prefix.
        """, action="store_true")

    args = parser.parse_args()

    if not args.username and not USERNAME:
        raise Exception('Please provide your Kippt username.')

    if not args.token and not API_TOKEN:
        raise Exception('Please provide your Kippt API token.')

    username = args.username or USERNAME
    token = args.token or API_TOKEN
    location = args.location or os.getcwd()
    raw_file_name = RAW_FILE_NAME
    structured_file_name = STRUCTURED_FILE_NAME
    prefix = PREFIX_TIME_FORMAT

    if not args.no_prefix:
        if args.prefix:
            prefix = args.prefix

        raw_file_name = '%s_%s' % (strftime(prefix, localtime()),
                                        raw_file_name)
        structured_file_name = '%s_%s' % (strftime(prefix, localtime()),
                                               structured_file_name)

    backup = kipptbackup.KipptBackup(username=username, api_token=token)
    with open(os.path.join(location, raw_file_name), 'w') as f:
        f.write(json.dumps(backup.raw_backup()))
    with open(os.path.join(location, structured_file_name), 'w') as f:
        f.write(json.dumps(backup.structured_backup()))

backup()
