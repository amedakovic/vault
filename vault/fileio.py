from pathlib import Path
import os
import subprocess
from rich.console import Console
from rich.markdown import Markdown
from rich.tree import Tree
from rich.prompt import Prompt

console = Console()

def open_editor(filename: str, context=None):
    editor = os.environ.get('EDITOR', 'nano' if os.name != 'nt' else 'notepad')
    try:
        if context is not None:
            with context:
                subprocess.run([editor, filename], check=True)
        else:
            subprocess.run([editor, filename], check=True)
    except FileNotFoundError:
        console.print(f"[red]Error opening editor on note {filename}[/red]")

def _resolve(working_directory: str, file_name: str) -> tuple[str, str]:
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    target_file = os.path.normpath(os.path.join(abs_path, file_name))
    if os.path.commonpath([abs_path, target_file]) != abs_path:
        raise ValueError(f"Path traversal detected: {target_file}")
    return abs_path, target_file

def add_note(working_directory: str, file_name: str, context=None):
    abs_path, target_file = _resolve(working_directory, file_name + ".md")
    os.makedirs(abs_path, exist_ok=True)
    Path(target_file).touch()
    open_editor(target_file, context=context)

def read_note(working_directory: str, file_name: str):
    _, target_file = _resolve(working_directory, file_name + ".md")
    if not os.path.isfile(target_file):
        console.print(f"[red]Error: note not found or is not a regular note: {target_file}[/red]")
        return
    with open(target_file) as f:
        console.print(Markdown(f.read()))

def _get_dir_entries(directory: str) -> list[tuple[str, str, bool]]:
     entries = []
     for name in sorted(os.listdir(directory)):
         path = os.path.join(directory, name)
         entries.append((name, path, Path(path).is_dir()))
     return entries

def _build_tree(directory: str, tree: Tree) -> None:
    for name,path,is_dir in _get_dir_entries(directory):
        if is_dir:
            branch = tree.add(f"[bold blue]{name}[/bold blue]")
            _build_tree(path, branch)
        else:
            tree.add(f"[green]{name}[/green]")

def get_notes_list(working_directory: str):
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    if not Path(abs_path).is_dir():
        console.print(f"[red]Error: {abs_path} is not a directory[/red]")
        return
    tree = Tree("[bold]vault[/bold]")
    _build_tree(abs_path, tree)
    console.print(tree)

def edit_note(target_file: str, context=None):
    if os.path.isfile(target_file) is False:
        console.print(f"[red]Error[/red] Note not found!")
        return
    open_editor(target_file, context)

def _delete_note(target_file: str):
    if os.path.isfile(target_file) is False:
        console.print(f"[red]Error[/red] Note not found!")
        return
    os.remove(target_file)

def delete_note(working_directory: str, file_name: str):
    confirmation = Prompt.ask(f"Are you sure you want to delete note {file_name}", default="n", choices=["y", "n"])
    if confirmation[0] == "n":
        return
    _, target_file = _resolve(working_directory, file_name + ".md")
    _delete_note(target_file)
    console.print(f"Note [red]{file_name}[/red] deleted")

def setup_config():
   vault_default = "~/.vault/" 
   config_file = "vault.config"
   abs_path, target_file = _resolve(vault_default, config_file)

   if os.path.isfile(target_file) is True:
       return
   os.makedirs(abs_path, exist_ok=True)
   Path(target_file).touch()
   with open(target_file, "w") as f:
       _ = f.write("# Directory where vault should be opened, notes written by default here\n")
       _ = f.write("vault_dir =  ~/.vault/\n")

def read_config() -> str:
   vault_config_file = "~/.vault/vault.config" 
   abs_path = os.path.abspath(os.path.expanduser(vault_config_file))
   vault_dir: str = ""

   if os.path.isfile(abs_path) is False:
       console.print(f"[red]Error[/red] reading config file ({vault_config_file})")

   with open(abs_path) as f:
       while True:
           line = f.readline().strip()
           if line.startswith("vault_dir"):
              value_index = line.find("=")
              vault_dir = line[value_index+1:].strip()
              break

   return vault_dir

