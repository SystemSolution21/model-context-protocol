from typing import Any
from mcp.server import FastMCP
from pathlib import Path

# Initialize the FastMCP server
mcp = FastMCP(name="notes")

# Get the current file path
current_dir: Path = Path(__file__).parent
note_file: Path = current_dir / "notes.txt"


# Do notes file exists
def note_file_exists() -> None:
    if not note_file.exists():
        with open(file=note_file, mode="w") as f:
            f.write("")


# Tool: Read notes
@mcp.tool()
async def read_notes() -> str:
    """
    Read all notes from the notes.txt file.

    Returns:
        str: The content of the notes file if it exists and has content,
             otherwise returns a default message.
    """
    note_file_exists()
    with open(file=note_file, mode="r") as f:
        content: str = f.read().strip()
    return content or "No notes yet!."


# Tool: Add notes
@mcp.tool()
async def add_notes(notes: str) -> str:
    """
    Append new notes to the notes.txt file.

    Args:
        notes (str): The text content to add as a new note.

    Returns:
        str: A success message confirming the note was added.
    """
    note_file_exists()
    with open(file=note_file, mode="a") as f:
        f.write(f"{notes}\n")
    return "Notes added successfully!"


# Resource: Get latest notes
@mcp.resource(uri="notes://latest")
async def get_latest_notes() -> str:
    """
    Retrieve the most recent note from the notes.txt file.

    Returns:
        str: The last line from the notes file if it exists and has content,
             otherwise returns a default message.
    """
    note_file_exists()
    with open(file=note_file, mode="r") as f:
        lines: list[str] = f.readlines()
    return lines[-1].strip() if lines else "No notes yet!."


# Prompt: Notes summary prompt
@mcp.prompt()
async def notes_summary_prompt() -> str:
    """
    Generate a prompt for summarizing all notes in the notes.txt file.

    This function reads the content of the notes file and creates a prompt
    requesting a summary of the notes. If no notes exist, it returns a
    default message.

    Returns:
        str: A prompt string containing either the notes to be summarized
             or a message indicating no notes exist.
    """
    note_file_exists()
    with open(file=note_file, mode="r") as f:
        content: str = f.read().strip()
    if not content:
        return "No notes yet!."
    return f"Summarize the following notes: {content}"


# Entry point for the FastMCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
