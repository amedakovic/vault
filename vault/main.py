import typer
from fileio import write_note, read_note, get_notes_list
app = typer.Typer()
dir = "~/.vault/"

@app.command()
def list():
    print("List command")
    get_notes_list(dir)

@app.command()
def write(note_name: str):
    print("Write command")
    write_note(dir, note_name)

@app.command()
def view(note_name: str):
    print("View command")
    read_note(dir, note_name)

if __name__ == "__main__":
    app()
