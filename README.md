# vault

A obsidian-lite terminal-based note-taking tool. Using rich for displaying in the console and textual for the simple tui.

## Features

- Create, view, edit, and delete markdown notes
- Search notes by content
- Wiki-style links between notes (`[[note-name]]`)
- Graph view of note connections

### Commands

| Command | Description |
|---|---|
| `tui` | Open the interactive terminal UI |
| `add <name>` | Create a new note |
| `view <name>` | View a note |
| `edit <name>` | Edit a note |
| `delete <name>` | Delete a note |
| `list` | List all notes |
| `search <query>` | Search notes by content |
| `links <name>` | Show links to and from a note |
| `graph` | Show the full link graph |
| `config` | Open the config file |

## Configuration

On first run, vault creates `~/.vault/vault.config` with the default vault directory set to `~/.vault/`. Edit this file to change where notes are stored.

## Linking Notes

Use `[[note-name]]` syntax inside any note to create a link. The `links` and `graph` commands will display these connections.
