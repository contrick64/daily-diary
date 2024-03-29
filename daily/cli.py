import argparse
from datetime import datetime

from .config import load_conf
from .journal import add_entry, add_write_headers
from .utils import make_dirpath, open_in_editor, wrap_file

conf = load_conf()

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

    parser.set_defaults(command="write")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    today_file = make_dirpath(conf['journal_dir']).joinpath(datetime.now().strftime(conf['filename_format']))
    match args.command:
        case 'add':
            # print(f'write entry {args.title}: {args.entry}')
            add_entry(today_file, args.mood[0], args.mood[1:],args.entry)
            return # skip opening editor
        case 'write':
            add_write_headers(today_file)
        case 'edit':
            pass
    open_in_editor(today_file)
    wrap_file(today_file,conf['wrap_width'])
    return

if __name__ == "__main__":
    main()