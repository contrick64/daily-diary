from datetime import datetime
import re

def load_conf():
    # here I am using %o for entry mood character, %O for mood words
    # and %E for entry text
    # the directives unaffected by strftime are ioqvEJKLNOQ
    config = {
        "journal_dir": "~/notes/daily",
        "filename_format": "%Y-%m-%d_log.md",
        "h1_title_format": "%Y-%m-%d daily log",
        "h2_inline_format": '%I:%M %p %o (%O)\n%E',
        "h2_format": '%I:%M %p',
        "wrap_width": 54
    }
    
    return config

def parse_time_format_string(string, **kwargs):
    new_directives = {
        'o':kwargs.get('mood_char',''),
        'O':kwargs.get('mood_words',''),
        'E':kwargs.get('entry','')
    }
    string = datetime.now().strftime(string)
    for directive,value in new_directives.items():
        string = re.sub('%'+directive,value,string)
    return string