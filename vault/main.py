import typer
from fileio import add_note, read_note, get_notes_list, delete_note, edit_note, delete_note, read_config, setup_config, open_editor
from search import search_notes
from pathlib import Path
app = typer.Typer()
setup_config()

VAULT_DIR = read_config()

@app.command()
def config():
    open_editor(str(Path.home() / ".vault" / "vault.config"))

@app.command()
def list():
    get_notes_list(VAULT_DIR)

@app.command()
def edit(note_name: str):
    edit_note(VAULT_DIR, note_name)

@app.command()
def add(note_name: str):
    add_note(VAULT_DIR, note_name)

@app.command()
def delete(note_name: str):
    delete_note(VAULT_DIR, note_name)

@app.command()
def view(note_name: str):
    read_note(VAULT_DIR, note_name)

@app.command()
def search(search_string: str):
    search_notes(VAULT_DIR, search_string)

if __name__ == "__main__":
    app()
