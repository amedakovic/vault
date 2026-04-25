import typer
from fileio import write_note 
app = typer.Typer()

@app.command()
def list():
    print("List command")

@app.command()
def write(note_name: str):
    print("Write command")
    write_note("~/.vault/", note_name)

@app.command()
def view():
    print("View command")

if __name__ == "__main__":
    app()
