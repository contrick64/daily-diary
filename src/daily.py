import argparse
import configparser
from datetime import datetime
import os
import re
import subprocess
from textwrap import wrap
from pathlib import Path
import textwrap

# here I am using %o for entry mood character, %O for mood words
# and %E for entry text
# the directives unaffected by strftime are ioqvEJKLNOQ
journal_dir = "~/notes/daily"
filename_format = "%Y-%m-%d_log.md"
h1_title_format = "%Y-%m-%d daily log"
h2_inline_format = '%I:%M %p %o (%O)\n%E'
h2_format = '%I:%M %p'
wrap_width = 54

def make_dirpath(path):
    path = re.sub(r"^~",str(Path.home()),path)
    path = Path(path)
    return path

def parse_format_string(string, **kwargs):
    new_directives = {
        'o':kwargs.get('mood_char',''),
        'O':kwargs.get('mood_words',''),
        'E':kwargs.get('entry','')
    }
    string = datetime.now().strftime(string)
    for directive,value in new_directives.items():
        string = re.sub('%'+directive,value,string)
    return string

def append_or_create_file(file,contents):
    if not re.match(r'\n$',contents):
        contents+='\n'
    with open(file, 'a+') as f:
        f.write(contents)
    return

def add_write_headers(file):
    file = Path(file)
    now = datetime.now()
    contents = ""
    if not file.exists():
        contents += now.strftime("# "+h1_title_format)
    contents += now.strftime("\n\n## "+h2_format+" ")
    append_or_create_file(file,contents)
    return

def add_entry(file, mood_char:str, mood_words:list, entry:str):
    file = Path(file)
    now = datetime.now()
    contents = ""
    if not file.exists():
        contents += now.strftime("# "+h1_title_format)
    entry_vars = {
        'mood_char':mood_char,
        'mood_words':', '.join(mood_words),
        'entry':wrap_preserving_newlines(entry[0],wrap_width)
    }
    contents += now.strftime("\n\n## "+parse_format_string(h2_inline_format,**entry_vars))
    append_or_create_file(file,contents)
    return

def open_in_editor(file):
    # Open a file in an editor
    file = Path(file)
    editor = os.environ.get('EDITOR','vi')
    if editor.rpartition('/')[2] in ['vi','vim']:
        exit_code = subprocess.call([editor, "+normal G$i", "+startinsert!", file])
        return exit_code
    exit_code = subprocess.call([editor, file])
    return exit_code

def wrap_file(file,wrap_width):
    with open(file, 'r') as f:
        contents = f.read()
        contents = wrap_preserving_newlines(contents,wrap_width)
    with open(file, 'w') as f:
        f.write(contents)
    return

def wrap_preserving_newlines(string_to_wrap,wrap_width):
    wrapper = textwrap.TextWrapper(width=wrap_width)
    lines = string_to_wrap.split('\n')
    line_list = [wrapper.fill(i) for i in lines]
    string_with_newlines = '\n'.join(line_list)
    return string_with_newlines

def load_conf(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def parse_args():
    parser = argparse.ArgumentParser(description="Make an entry in your markdown diary.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    all_entry_parser = argparse.ArgumentParser(add_help=False)
    all_entry_parser.add_argument('-w', '--wrap-file', action="store_true", help="Wrap the entire contents of today's entry")

    write_parser = subparsers.add_parser('write', parents=[all_entry_parser], help="(DEFAULT) Write an entry to todays file, create it if not exists")

    add_entry_parser = subparsers.add_parser('add', parents=[all_entry_parser], help="Add an entry inline")
    add_entry_parser.add_argument('-m', '--mood', metavar=('+/-/=', 'mood'), required=True, nargs='+', help="The mood character and word(s) to be included")
    add_entry_parser.add_argument('-e', '--entry',nargs=1, required=True, help="Write the text to be entered inline")

    edit_parser = subparsers.add_parser('edit', parents=[all_entry_parser], help="Edit today's entry without adding any headers")

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