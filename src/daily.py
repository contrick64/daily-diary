import argparse
import configparser
from datetime import datetime
import re
from textwrap import wrap
from pathlib import Path

# here I am using %L for entry title, and %E for entry text
new_title_format = "# %Y-%m-%d daily log"
append_title_format = '''## %I:%M %p (%L)
%E'''
title_format = '''## %I:%M %p
'''
wrap_width = 54

def parse_format_string(string, **kwargs):
    new_directives = {
        'L':kwargs.get('title',''),
        'E':kwargs.get('entry','')
    }
    string = datetime.now().strftime(string)
    for directive,value in new_directives.items():
        string = re.sub('%'+directive,value,string)
    return string

def make_header(datetime):
    # Write an h2 into the file with the current time (or configurable)
    return

def open_in_editor(file):
    # Open a file in an editor
    return

def load_conf(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def parse_args():
    parser = argparse.ArgumentParser(description="Make an entry in your markdown diary.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    write_parser = subparsers.add_parser('write', help="(DEFAULT) Write an entry to todays file, create it if not exists")
    write_parser.add_argument('-a', '--append', action='store_true', help="append to last entry without new header line")
    write_parser.add_argument('-t', '--title', help="Write the header to be entered inline")
    write_parser.add_argument('-e', '--entry', help="Write the text to be entered inline")

    list_parser = subparsers.add_parser('list', help="List existing entries")

    parser.set_defaults(command="write")

    args = parser.parse_args()
    return args

def main(args):
    # conf = load_conf()
    match args.command:
        case 'list':
            print('list of dailies!')
            return
        case 'write':
            print(f'write entry {args.title}: {args.entry}')
            return


if __name__ == "__main__":
    args = parse_args()
    main(args)