from pathlib import Path
from fileio import _resolve
import os
from rich.console import Console
from rich.tree import Tree
import re

console = Console()

def search_links_in_note(note_name: str) -> list[str]:
    regex = re.compile(r"\[\[(.+?)\]\]")
    matches: list[str] = []
    with open(note_name, "r") as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                matches.append(match.group(1))
    return matches

def search_linked_by(directory: str, note_name: str) -> list[str]:
    linkedby: list[str] = []
    for entry in os.listdir(directory):
        if entry.endswith(".config"):
            continue
        path = os.path.join(directory, entry)
        if Path(path).is_dir():
            linkedby.extend(search_linked_by(path, note_name))
        else:
            links = search_links_in_note(path)
            if note_name in links:
                linkedby.append(entry[:-3])
    return linkedby

def note_links(working_directory: str, note_name: str):
    abs_path, target_file = _resolve(working_directory, note_name + ".md")
    if not os.path.isfile(target_file):
        console.print(f"[red]Error: Note not found or is not a regular file: {target_file}[/red]")
        return
    links = search_links_in_note(target_file)
    linkedby = search_linked_by(abs_path, note_name)
    tree = Tree(f"[bold]{note_name}[/bold]")
    if len(links) > 0:
        linkes_to_branch = tree.add("Linkes to")
        for link in links:
            linkes_to_branch.add(f"-> {link}")
    if len(linkedby) > 0:
        linked_by_branch = tree.add("Linked by")
        for link in linkedby:
            linked_by_branch.add(f"<- {link}")
    console.print(tree)

def build_full_tree(directory: str, tree: Tree):
    for entry in os.listdir(directory):
        if entry.endswith(".config"):
            continue
        path = os.path.join(directory, entry)
        if Path(path).is_dir():
            build_full_tree(path, tree)
        else:
            links = search_links_in_note(path)
            branch = tree.add(f"[blue]{entry}[/blue]")
            if len(links) <= 0:
                branch.add("No links found in note")
                continue
            for link in links:
                branch.add(f"-> {link}")

def full_graph(working_directory:str):
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    if os.path.isfile(abs_path):
        console.print(f"[red]Error: given a note: {abs_path}[/red]")
        return
    tree = Tree("Full graph")
    build_full_tree(abs_path, tree)
    console.print(tree)


