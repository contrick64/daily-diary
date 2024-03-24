import os
import re
from pathlib import Path
import subprocess
from textwrap import TextWrapper

def make_dirpath(path):
    path = re.sub(r"^~",str(Path.home()),path)
    path = Path(path)
    return path

def wrap_file(file,wrap_width):
    with open(file, 'r') as f:
        contents = f.read()
        contents = wrap_preserving_newlines(contents,wrap_width)
    with open(file, 'w') as f:
        f.write(contents)
    return

def wrap_preserving_newlines(string_to_wrap,wrap_width):
    wrapper = TextWrapper(width=wrap_width)
    lines = string_to_wrap.split('\n')
    line_list = [wrapper.fill(i) for i in lines]
    string_with_newlines = '\n'.join(line_list)
    return string_with_newlines

def open_in_editor(file):
    # Open a file in an editor
    file = Path(file)
    editor = os.environ.get('EDITOR','vi')
    exit_code = subprocess.call([editor, file])
    return exit_code