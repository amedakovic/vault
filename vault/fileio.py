from pathlib import Path
import os
from site import abs_paths
import subprocess
from rich.console import Console
from rich.markdown import Markdown
from rich.tree import Tree

console = Console()

def open_editor(filename: str):
    editor = os.environ.get('EDITOR', 'nano' if os.name != 'nt' else 'notepad')
    try:
        subprocess.run([editor, filename], check=True)
    except FileNotFoundError:
        console.print(f"[red]Error opening editor on file {filename}[/red]")

def _resolve(working_directory: str, file_name: str) -> tuple[str, str]:
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    target_file = os.path.normpath(os.path.join(abs_path, file_name))
    if os.path.commonpath([abs_path, target_file]) != abs_path:
        raise ValueError(f"Path traversal detected: {target_file}")
    return abs_path, target_file

def add_note(working_directory: str, file_name: str):
    abs_path, target_file = _resolve(working_directory, file_name + ".md")
    os.makedirs(abs_path, exist_ok=True)
    Path(target_file).touch()
    open_editor(target_file)

def read_note(working_directory: str, file_name: str):
    _, target_file = _resolve(working_directory, file_name + ".md")
    if not os.path.isfile(target_file):
        console.print(f"[red]Error: File not found or is not a regular file: {target_file}[/red]")
        return
    with open(target_file) as f:
        console.print(Markdown(f.read()))

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
    if not Path(abs_path).is_dir():
        console.print(f"[red]Error: {abs_path} is not a directory[/red]")
        return
    tree = Tree(f"[bold]{abs_path}[/bold]")
    _build_tree(abs_path, tree)
    console.print(tree)

def delete_note(working_directory: str, file_name: str):
    _, target_file = _resolve(working_directory, file_name + ".md")
    if not os.path.isfile(target_file):
        console.print(f"[red]Error: File not found or is not a regular file: {target_file}[/red]")
        return
    Path(target_file).unlink()
    console.print(f"[blue]Note: {file_name} [bold]deleted[/bold][/blue]")

def edit_note(working_directory: str, file_name: str):
    _, target_file = _resolve(working_directory, file_name + ".md")
    if os.path.isfile(target_file) is False:
        console.print(f"[red]Error[/red] Note not found!")
        return
    open_editor(target_file)
