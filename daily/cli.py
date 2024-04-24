import argparse
from datetime import datetime

from .config import load_conf
from .journal import add_entry, add_write_headers
from .view import view_entries
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

    view_parser = subparsers.add_parser('view', parents=[all_entry_parser], help="Print entries to the terminal")
    view_parser.add_argument('-d','--days', type=int, help="The number of days back to display (cannot be used with --to or --from)")
    view_parser.add_argument('--no-color',dest='color', action="store_false", help="Turn off colors in the printed entries")
    view_parser.add_argument('-f', '--from',dest='from_date', help="Start date of entries to print in YYYY-MM-DD format (cannot be used with --days)")
    view_parser.add_argument('-t','--to',dest='to_date', help="End date of entries to print in YYYY-MM-DD format (cannot be used with --days)")

    parser.set_defaults(command="write")

    args = parser.parse_args()

    if args.days is not None and (args.to_date or args.from_date):
        view_parser.error("--days cannot be set with --from or --to")
    if args.to_date is not None and args.from_date is None:
        parser.error("--from must be set when using --to")

    if args.to_date:
        args.to_date = datetime.strptime(args.to_date,conf['input_date_format'])
    if args.from_date:
        args.from_date = datetime.strptime(args.from_date,conf['input_date_format'])

    return args

def main():
    args = parse_args()
    today_file = make_dirpath(conf['journal_dir']).joinpath(datetime.now().strftime(conf['filename_format']))

    match args.command:
        case 'add':
            add_entry(today_file, args.mood[0], args.mood[1:],args.entry)
            print(f'Added entry to {today_file}')

        case 'write':
            add_write_headers(today_file)
            open_in_editor(today_file)
            wrap_file(today_file,conf['wrap_width'])
            print(f"Added entry to {today_file}")

        case 'edit':
            open_in_editor(today_file)
            wrap_file(today_file,conf['wrap_width'])
            print(f"Edited {today_file}")

        case 'view':
            view_entries(conf['journal_dir'],conf['filename_format'],num_days=args.days,color=args.color,start_date=args.from_date,end_date=args.to_date)

    return

if __name__ == "__main__":
    main()