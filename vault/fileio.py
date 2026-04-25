from pathlib import Path
import os
import subprocess
from rich.console import Console
from rich.markdown import Markdown
from rich.tree import Tree

def open_editor(filename: str):
    # get editor from env variable
    editor = os.environ.get('EDITOR', 'nano' if os.name != 'nt' else 'notepad')
    try:
        # try to open the file using subprocess module
        subprocess.run( [editor, filename], check=True)
    except FileNotFoundError:
        print(f"Error opening editor on file {filename}")

# append .md to the file name, and create it and then open in editor
def write_note(working_directory: str, file_name: str):
    file_name = file_name + ".md"
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    target_file = os.path.normpath(os.path.join(abs_path, file_name))

    if os.path.commonpath([abs_path, target_file]) != abs_path:
        raise ValueError(f"Path traversal detected: {target_file}")

    os.makedirs(abs_path, exist_ok=True)
    open(target_file, 'a').close()
    open_editor(target_file)

def read_note(working_directory: str, file_name: str):
    file_name = file_name + ".md"

    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    target_file = os.path.normpath(os.path.join(abs_path, file_name))
    console = Console()

    if os.path.commonpath([abs_path, target_file]) != abs_path:
        raise ValueError(f"Path traversal detected: {target_file}")
    if os.path.isfile(target_file) is False:
        print(f"Error: File not found or is not a regular file: {target_file}")
        return

    with open(target_file) as f:
        markup  = Markdown(f.read())
        console.print(markup)

def _build_tree(directory: str, tree: Tree) -> None:
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if Path(path).is_dir():
            branch = tree.add(f"[bold blue]{entry}[/bold blue]")
            _build_tree(path, branch)
        else:
            tree.add(f"[green]{entry}[/green]")

def get_notes_list(working_directory: str):
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    console = Console()
    if not Path(abs_path).is_dir():
        print(f"Error: {abs_path} is not a directory")
        return
    tree = Tree(f"[bold]{abs_path}[/bold]")
    _build_tree(abs_path, tree)
    console.print(tree)

