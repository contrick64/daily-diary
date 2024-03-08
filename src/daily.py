import argparse
import configparser
from pathlib import Path

def load_conf(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def parse_args():
    parser = argparse.ArgumentParser(description="Make an entry in your markdown diary.")
    parser.add_argument('-a', '--append', action='store_true', help="append to last entry without new header line")
    args = parser.parse_args()

def write_new_file(date):
    # Write a file named YYYY-MM-DD_log.md (make configurable eventually) with an h1
    return

def write_time_header(datetime):
    # Write an h2 into the file with the current time (or configurable)
    return

def open_in_editor(file):
    # Open a file in an editor
    return

def main():
    args = parse_args()
    

if __name__ == "__main__":
    main()