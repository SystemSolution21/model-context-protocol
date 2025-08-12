# notes.py
"""
This module provides a simple note-taking application using the FastMCP framework.
It includes tools for creating, reading, editing, deleting, and listing notes.
Each note is stored as a separate file in the 'notes_data' directory.
"""

import re
import unicodedata
from pathlib import Path

from mcp.server import FastMCP

# Initialize FastMCP server
mcp = FastMCP(name="notes")

# Current file path
current_dir: Path = Path(__file__).parent
notes_dir: Path = current_dir / "notes_data"


# --- Helper Functions ---


def _sanitize_title_to_filename(title: str) -> str:
    """
    Sanitizes a string to be used as a valid filename.
    """
    s: str = (
        unicodedata.normalize("NFKD", title)
        .encode(encoding="ascii", errors="ignore")
        .decode(encoding="ascii")
    )
    s: str = re.sub(pattern=r"[^\w\s-]", repl="", string=s).strip().lower()
    s: str = re.sub(pattern=r"[-\s]+", repl="-", string=s)
    return s + ".txt"


def _get_note_path(title: str) -> Path:
    """
    Gets the full path for a note from its title.
    Ensures the notes directory exists.
    """
    notes_dir.mkdir(exist_ok=True)
    filename = _sanitize_title_to_filename(title)
    return notes_dir / filename


# --- Tools ---


@mcp.tool()
async def list_notes() -> str:
    """
    Lists all available notes by their title.

    Returns:
        str: A list of available note titles, or a message if none exist.
    """
    notes_dir.mkdir(exist_ok=True)
    note_files: list[Path] = sorted(notes_dir.glob(pattern="*.txt"))
    if not note_files:
        return "No notes found. You can create one with 'add_note'."
    titles: list[str] = [f.stem.replace("-", " ").title() for f in note_files]
    return "Available notes:\n- " + "\n- ".join(titles)


@mcp.tool()
async def add_note(title: str, content: str) -> str:
    """
    Creates a new note with a given title and content.

    Args:
        title (str): The title for the new note.
        content (str): The text content of the new note.

    Returns:
        str: A success or failure message.
    """
    if not title.strip() or not content.strip():
        return "Error: Title and content cannot be empty."
    note_path: Path = _get_note_path(title=title)
    if note_path.exists():
        return f"Error: A note with the title '{title}' already exists."
    note_path.write_text(content.strip(), encoding="utf-8")
    return f"Note '{title}' created successfully."


@mcp.tool()
async def read_note(title: str) -> str:
    """
    Reads the content of a specific note.

    Args:
        title (str): The title of the note to read.

    Returns:
        str: The content of the note, or an error message if not found.
    """
    note_path: Path = _get_note_path(title=title)
    try:
        return note_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: Note with title '{title}' not found."


@mcp.tool()
async def delete_note(title: str) -> str:
    """
    Deletes a specific note by its title.

    Args:
        title (str): The title of the note to delete.

    Returns:
        str: A success or failure message.
    """
    note_path: Path = _get_note_path(title=title)
    try:
        note_path.unlink()
        return f"Note '{title}' deleted successfully."
    except FileNotFoundError:
        return f"Error: Note with title '{title}' not found."


@mcp.tool()
async def edit_note(title: str, new_content: str) -> str:
    """
    Edits an existing note, replacing its content.

    Args:
        title (str): The title of the note to edit.
        new_content (str): The new text content for the note.

    Returns:
        str: A success or failure message.
    """
    if not new_content.strip():
        return "Error: Cannot replace a note with empty content."
    note_path: Path = _get_note_path(title=title)
    if not note_path.exists():
        return f"Error: Note with title '{title}' not found."
    note_path.write_text(data=new_content.strip(), encoding="utf-8")
    return f"Note '{title}' edited successfully."


# --- Resources & Prompts ---


@mcp.resource(uri="notes://latest")
async def get_latest_notes() -> str:
    """
    Retrieve the content of the most recently modified note.

    Returns:
        str: The content of the latest note if it exists,
             otherwise returns a default message.
    """
    notes_dir.mkdir(exist_ok=True)
    try:
        latest_file: Path = max(
            notes_dir.glob(pattern="*.txt"), key=lambda f: f.stat().st_mtime
        )
        return latest_file.read_text(encoding="utf-8")
    except (FileNotFoundError, ValueError):
        return "No notes yet!."


@mcp.prompt()
async def notes_summary_prompt() -> str:
    """
    Generate a prompt for summarizing all available notes.

    This function reads the content of all note files and creates a prompt
    requesting a summary.

    Returns:
        str: A prompt string containing either the notes to be summarized
             or a message indicating no notes exist.
    """
    notes_dir.mkdir(exist_ok=True)
    all_content: list[str] = []
    for note_path in sorted(notes_dir.glob(pattern="*.txt")):
        title: str = note_path.stem.replace("-", " ").title()
        content: str = note_path.read_text(encoding="utf-8")
        all_content.append(f"--- Note: {title} ---\n{content}")

    if not all_content:
        return "No notes yet!."

    return "Summarize the following notes:\n\n" + "\n\n".join(all_content)


# Entry point for the FastMCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
