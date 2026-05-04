from typing import override
from rich import text
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import MarkdownViewer, Welcome,Tree, Label, Button, Input
from textual.containers import Grid
from textual.screen import ModalScreen
from fileio import _get_dir_entries, _delete_note, add_note, edit_note
from pathlib import Path
import os
class NewNoteNameInput(ModalScreen[bool]):
    """A modal screen to confirm deletion."""

    CSS ="""
    NewNoteNameInput {
    align: center middle;
}

#dialog {
    width: 30;
    height: 5;
    border: thick $background 80%;
    background: $surface;
}
"""
    def compose(self) -> ComposeResult:
        # A simple grid to center the dialog
        with Grid(id="dialog"):
            yield Input(placeholder="New Note")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value.strip():
            self.dismiss(event.value)
        else:
            # dismiss with None
            self.dismiss(None)

class ConfirmDelete(ModalScreen[bool]):
    """A modal screen to confirm deletion."""

    CSS ="""
    ConfirmDelete {
    align: center middle;
}

#dialog {
    grid-size: 2;
    grid-gutter: 1;
    grid-rows: 1fr 3;
    padding: 0 1;
    width: 45;
    height: 8;
    border: thick $background 80%;
    background: $surface;
}

#question {
    column-span: 2;
    content-align: center middle;
    text-style: bold;
}
Button:focus {
    text-style: bold reverse;
    border: tall $accent;
}
"""
    def compose(self) -> ComposeResult:
        # A simple grid to center the dialog
        with Grid(id="dialog"):
            yield Label("Are you sure you want to delete this file?", id="question")
            yield Button("Delete", variant="error", id="delete")
            yield Button("Cancel", variant="primary", id="cancel")

    def on_mount(self) -> None:
        # Manually focus the cancel button when the modal pops up
        self.query_one("#cancel").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete":
            self.dismiss(True)
        else:
            self.dismiss(False)
class MyApp(App):
    #CSS = "~/Projects/vault/vault/tui_css.css"
    CSS = """

#tree-side {
        width: 20%;
        height: 100%;
        border-right: vkey $accent;
}

#view-side {
        width: 80%;
        height: 100%;
}
"""
    def __init__(self, directory: str):
        super().__init__()
        self._working_directory = directory
        self.notes: Tree[str] = Tree("vault", id="tree-side")
        self.viewer = MarkdownViewer(id="view-side", show_table_of_contents=False)

    def _build_tree(self, directory: str, node):
        for name,path,is_dir in _get_dir_entries(directory):
            if is_dir:
                branch = node.add(name, expand=False)
                self._build_tree(path, branch)
            else:
                if not name.endswith(".config"):
                    node.add_leaf(name[:-3], data=path)
        
    def _get_tree(self):
        abs_path = os.path.abspath(os.path.expanduser(self._working_directory))
        if not Path(abs_path).is_dir():
            return self.notes
        self.notes.root.expand()
        #notes = tree.root.add("Notes", expand=True)
        self._build_tree(abs_path, self.notes.root)

    async def on_tree_node_highlighted(self, event: Tree.NodeSelected) -> None:
        path: str| None = event.node.data
        await self._show_in_viewer(path)

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self.notes
            yield self.viewer

    async def on_key(self, event: events.Key) -> None:
        if event.key == "j":
            self.notes.action_cursor_down()
        if event.key == "k":
            self.notes.action_cursor_up()
        if event.key == "l":
            self.notes.action_toggle_node()
        if event.key == "d":
            self.push_screen(ConfirmDelete(), callback=self.handle_delete_note)
        if event.key == "a":
            self.push_screen(NewNoteNameInput(), callback=self.handle_add_note)
        if event.key == "e":
            await self.handle_edit_note()

    async def handle_edit_note(self):
        node = self.notes.cursor_node
        if node is None:
            return
        note_name = str(node.label)
        edit_note(self._working_directory, note_name, context=self.suspend())
        path = node.data
        await self._show_in_viewer(path)

    async def _show_in_viewer(self, path: str | None):
        if path is None:
            return
        if os.path.isfile(path):
            await self.viewer.go(path)


    def handle_add_note(self, note_name):
        if note_name is None:
            return
        add_note(self._working_directory, note_name, context=self.suspend())
        self.notes.clear()
        self._get_tree()

    def handle_delete_note(self, should_delete:bool):
        if should_delete is False:
            return
        node = self.notes.cursor_node
        if node is None:
            return
        note_name = str(node.label)
        _delete_note(self._working_directory, note_name)
        self.notes.clear()
        self._get_tree()

    def on_mount(self) -> None:
        self._get_tree()

def run_tui(working_directory: str):
    app = MyApp(working_directory)
    app.run()
