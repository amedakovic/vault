from itertools import count
import os
from pathlib import Path
import re
from rich.console import Console

console = Console()

def _build_found_string_dic(directory: str, regex: str, found: dict[str, list[str]]):
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if Path(path).is_dir():
            _build_found_string_dic(path, regex, found)
        else:
            with open(path) as f:
                for line in f:
                    if re.search(regex, line):
                        line = line.replace(regex, f"[green]{regex}[/green]")
                        if path in found:
                            found[path].append(line)
                        else:
                            found[path] = [line]

def search_notes(working_directory: str, search_string: str):
    abs_path = os.path.abspath(os.path.expanduser(working_directory))
    
    if not Path(abs_path).is_dir():
        console.print(f"[red]Error: {abs_path} is not a direcotry[/red]")

    pattern = rf"{re.escape(search_string)}"
    found: dict[str, list[str]] = {}
    _build_found_string_dic(abs_path, pattern, found)
    console.print(f"String \"{search_string}\" found in {len(found)} notes")
    for line in found:
        note_len = len(os.path.commonpath([line, abs_path]))
        print(f"{line[note_len+1:-3]}:")
        for foundStr in found[line]:
            console.print(f"\t{foundStr}")

