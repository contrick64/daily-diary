from datetime import datetime, timedelta
from pathlib import Path
from colorist import Color
import re

from .config import load_conf
from .utils import make_dirpath


conf = load_conf()

def get_file_contents(file_path: Path) -> str:
    if not file_path.exists():
        return ''
    with open(file_path, 'r') as file:
        return file.read()

def get_dated_file_path(dir: Path, date: datetime, filename_format: str) -> None:
    return dir.joinpath(date.strftime(filename_format))

def get_today_file_path(dir: Path, filename_format: str) -> None:
    return get_dated_file_path(dir, datetime.now(), filename_format)

def print_files_in_date_range(dir: Path, filename_format: str, start_date: datetime = datetime.now(), end_date: datetime = datetime.now(),color:bool=True) -> None:
    print(f"\nPrinting files from {start_date.strftime(conf['input_date_format'])} to {end_date.strftime(conf['input_date_format'])}")
    if start_date > end_date:
        print("Start date is after end date.")
        return
    date = start_date
    while date <= end_date:
        if get_file_contents(get_dated_file_path(dir, date, filename_format)) and date not in (start_date,end_date):
            print('\n==============\n')
        if color:
            print(colorize_markdown_string(get_file_contents(get_dated_file_path(dir, date, filename_format))), end='')
        else:
            print(get_file_contents(get_dated_file_path(dir,date,filename_format)),end='')
        date += timedelta(days=1)
    print()
    return

def print_today_file(dir: Path, filename_format: str) -> None:
    print(get_file_contents(get_today_file_path(dir, filename_format)))
    return

def print_number_of_days(dir: Path, filename_format: str, num_days: int,color:bool) -> None:
    print_files_in_date_range(dir, filename_format, datetime.now() - timedelta(days=num_days), datetime.now(),color=color)
    return

def colorize_markdown_string(string: str) -> str:
    # colorize headers
    string = re.sub(r'(^|\n)(# .*)(\n|$)', f'\\1{Color.BLUE}\\2{Color.OFF}\\3', string)
    string = re.sub(r'(^|\n)(## .*)(\n|$)', f'\\1{Color.CYAN}\\2{Color.OFF}\\3', string)
    string = re.sub(r'(?<=## \d\d:\d\d [AP]M )\+', f'{Color.GREEN}\\g<0>{Color.OFF}', string)
    string = re.sub(r'(?<=## \d\d:\d\d [AP]M )-', f'{Color.RED}\\g<0>{Color.OFF}', string)
    string = re.sub(r'(?<=## \d\d:\d\d [AP]M )=', f'{Color.YELLOW}\\g<0>{Color.OFF}', string)
    return string

def view_entries(dir: str, filename_format: str, num_days: int=1,color:bool=True) -> None:
    print_number_of_days(make_dirpath(dir),filename_format,num_days,color)
    return