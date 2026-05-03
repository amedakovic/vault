from typing import override
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import MarkdownViewer, Welcome, Tree
from fileio import _get_dir_entries
from pathlib import Path
import os

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
        path: str = event.node.data
        
        if path is None:
            return
        if os.path.isfile(path):
            await self.viewer.go(path)

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self.notes
            yield self.viewer

    def on_mount(self) -> None:
        self._get_tree()

    def on_button_pressed(self) -> None:
        self.exit()

def run_tui(working_directory: str):
    app = MyApp(working_directory)
    app.run()
