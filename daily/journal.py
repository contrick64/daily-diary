from datetime import datetime
from pathlib import Path
import re

from .config import load_conf, parse_time_format_string
from .utils import wrap_preserving_newlines

conf = load_conf()

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
        contents += now.strftime("# "+conf['h1_title_format'])
    contents += now.strftime("\n\n## "+conf['h2_format']+" ")
    append_or_create_file(file,contents)
    return

def add_entry(file, mood_char:str, mood_words:list, entry:str):
    file = Path(file)
    now = datetime.now()
    contents = ""
    if not file.exists():
        contents += now.strftime("# "+conf['h1_title_format'])
    entry_vars = {
        'mood_char':mood_char,
        'mood_words':', '.join(mood_words),
        'entry':wrap_preserving_newlines(entry[0],conf['wrap_width'])
    }
    contents += now.strftime("\n\n## "+parse_time_format_string(conf['h2_inline_format'],**entry_vars))
    append_or_create_file(file,contents)
    return