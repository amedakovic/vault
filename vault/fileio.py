from pathlib import Path
import os
import subprocess

def open_editor(filename: str):
    # get editor from env variable
    editor = os.environ.get('EDITOR', 'nano' if os.name != 'nt' else 'notepad')
    try:
        # try to open the file using subprocess module
        subprocess.run( [editor, filename], check=True)
    except FileNotFoundError:
        print(f"Error opening editor on file {filename}")

def write_note(working_directory: str, file_name: str):
    file_name = file_name + ".md"
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    target_file = os.path.normpath(os.path.join(abs_path, file_name))
    if os.path.commonpath([abs_path, target_file]) != abs_path:
        raise ValueError(f"Path traversal detected: {target_file}")
    os.makedirs(abs_path, exist_ok=True)
    open(target_file, 'a').close()
    open_editor(target_file)
