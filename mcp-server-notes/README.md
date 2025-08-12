# MCP Note-Taking Server

A robust, file-based note-taking application built with the Model Context Protocol (MCP). This server allows an AI model to create, read, update, delete, and list individual notes, making it a practical tool for managing information.

Each note is stored as a separate text file, making the system transparent and easy to manage outside of the MCP interface.

## Features & Tools

The server exposes the following tools for an AI to use:

- **`list_notes()`**: Lists the titles of all saved notes.
- **`add_note(title: str, content: str)`**: Creates a new note with a specific title and content.
- **`read_note(title: str)`**: Retrieves the full content of a note by its title.
- **`edit_note(title: str, new_content: str)`**: Updates the content of an existing note.
- **`delete_note(title: str)`**: Deletes a note by its title.
- **`notes_summary_prompt()`**: Generates a prompt for an AI to summarize the content of all notes.

## How It Works

- When you add a note, a new `.txt` file is created in the `notes_data` directory.
- The filename is a sanitized version of the note's title (e.g., "My Shopping List" becomes `my-shopping-list.txt`).
- All operations (read, edit, delete) are performed on these individual files based on the provided title.

## Requirements

- Python 3.13+
- `mcp[cli]`

## Running the Server

1. **Run in Development Mode:**
    This command starts a local proxy server, allowing you to inspect the communication between a client and your note-taking server.

    ```bash
    mcp dev notes.py
    ```

    - The MCP server will be listening on `localhost:6277`.
    - The MCP Inspector (a web-based client for testing) will be available at `http://localhost:6274`.

2. **Install Locally:**
    This command installs the server so it can be used by local AI applications that support MCP, like the Claude Desktop App.

    ```bash
    mcp install notes.py
    ```

## Example Usage Flow

1. **List existing notes:** `list_notes()` -> `No notes found. You can create one with 'add_note'.`
2. **Create a new note:** `add_note(title="Shopping List", content="- Milk\n- Bread\n- Eggs")` -> `Note 'Shopping List' created successfully.`
3. **Read the note:** `read_note(title="Shopping List")` -> `- Milk\n- Bread\n- Eggs`
4. **Edit the note:** `edit_note(title="Shopping List", new_content="- Milk\n- Bread\n- Eggs\n- Cheese")` -> `Note 'Shopping List' edited successfully.`
5. **Delete the note:** `delete_note(title="Shopping List")` -> `Note 'Shopping List' deleted successfully.`
