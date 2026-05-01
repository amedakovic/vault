import typer
from fileio import write_note, read_note, get_notes_list, delete_note
from search import search_notes
app = typer.Typer()
VAULT_DIR = "~/.vault/"

@app.command()
def list():
    get_notes_list(VAULT_DIR)

@app.command()
def write(note_name: str):
    write_note(VAULT_DIR, note_name)

@app.command()
def view(note_name: str):
    read_note(VAULT_DIR, note_name)

@app.command()
def search(search_string: str):
    search_notes(VAULT_DIR, search_string)

@app.command()
def delete(note_name: str):
    delete_note(VAULT_DIR, note_name)

if __name__ == "__main__":
    app()
