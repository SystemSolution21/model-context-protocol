# notes.py
"""
This module provides a simple note-taking application using the FastMCP framework.
It includes tools for reading and adding notes, a resource for retrieving the latest note,
and a prompt for summarizing all notes.
"""

from pathlib import Path

from mcp.server import FastMCP

# Initialize FastMCP server
mcp = FastMCP(name="notes")

# Current file path
current_dir: Path = Path(__file__).parent
note_file: Path = current_dir / "notes.txt"


# Tool: Read notes
@mcp.tool()
async def read_notes() -> str:
    """
    Read all notes from the notes.txt file.

    Returns:
        str: The content of the notes file if it exists and has content,
             otherwise returns a default message.
    """
    try:
        with open(file=note_file, mode="r") as f:
            content: str = f.read().strip()
        return content or "No notes yet!."
    except FileNotFoundError:
        return "No notes yet!."


# Tool: Add notes
@mcp.tool()
async def add_notes(notes: str) -> str:
    """
    Append new notes to the notes.txt file, with automatic numbering.

    Args:
        notes (str): The text content to add as a new note.

    Returns:
        str: A success message confirming the note was added, including its number.
    """
    if not notes.strip():
        return "Cannot add an empty note."

    last_number = 0
    try:
        with open(file=note_file, mode="r") as f:
            lines: list[str] = f.readlines()
        # Last numbered line to determine the next number
        for line in reversed(lines):
            line: str = line.strip()
            if line and "." in line:
                parts: list[str] = line.split(sep=".", maxsplit=1)
                if parts[0].isdigit():
                    last_number = int(parts[0])
                    break
    except FileNotFoundError:
        # File doesn't exist, start numbering from 1.
        pass

    next_number: int = last_number + 1
    with open(file=note_file, mode="a") as f:
        f.write(f"{next_number}. {notes}\n")
    return f"Note #{next_number} added successfully!"


# Tool: Delete a note
@mcp.tool()
async def delete_note(note_number: str) -> str:
    """
    Deletes a note by its number and re-numbers the remaining notes.

    Args:
        note_number (str): The number of the note to delete.

    Returns:
        str: A success or failure message.
    """
    if not note_number.strip().isdigit():
        return "Please provide a valid note number to delete."

    note_num = int(note_number)

    try:
        with open(file=note_file, mode="r") as f:
            lines: list[str] = f.readlines()
    except FileNotFoundError:
        return "No notes file found. Nothing to delete."

    if not lines:
        return "Notes file is empty. Nothing to delete."

    note_found = False
    updated_notes_content: list[str] = []
    for line in lines:
        stripped_line: str = line.strip()
        if not stripped_line:
            continue

        parts: list[str] = stripped_line.split(sep=".", maxsplit=1)
        if len(parts) == 2 and parts[0].isdigit():
            if int(parts[0]) == note_num:
                note_found = True
            else:
                updated_notes_content.append(parts[1].strip())

    if not note_found:
        return f"Note #{note_num} not found."

    with open(file=note_file, mode="w") as f:
        for i, content in enumerate(iterable=updated_notes_content, start=1):
            f.write(f"{i}. {content}\n")

    return f"Note #{note_num} deleted and notes re-numbered successfully."


# Tool: Edit a note
@mcp.tool()
async def edit_note(note_number: str, new_content: str) -> str:
    """
    Edits an existing note by its number.

    Args:
        note_number (str): The number of the note to edit.
        new_content (str): The new text content for the note.

    Returns:
        str: A success or failure message.
    """
    if not note_number.strip().isdigit():
        return "Please provide a valid note number to edit."

    note_num = int(note_number)

    if not new_content.strip():
        return "Cannot replace a note with empty content."

    try:
        with open(file=note_file, mode="r") as f:
            lines: list[str] = f.readlines()
    except FileNotFoundError:
        return "No notes file found. Nothing to edit."

    if not lines:
        return "Notes file is empty. Nothing to edit."

    note_found = False
    updated_lines: list[str] = []
    for line in lines:
        stripped_line: str = line.strip()
        parts: list[str] = stripped_line.split(".", 1)
        if len(parts) == 2 and parts[0].isdigit() and int(parts[0]) == note_num:
            updated_lines.append(f"{note_num}. {new_content.strip()}\n")
            note_found = True
        else:
            updated_lines.append(line)

    if not note_found:
        return f"Note #{note_num} not found."

    with open(file=note_file, mode="w") as f:
        f.writelines(updated_lines)

    return f"Note #{note_num} edited successfully."


# Resource: Get latest notes
@mcp.resource(uri="notes://latest")
async def get_latest_notes() -> str:
    """
    Retrieve the most recent note from the notes.txt file.

    Returns:
        str: The last line from the notes file if it exists and has content,
             otherwise returns a default message.
    """
    try:
        with open(file=note_file, mode="r") as f:
            lines: list[str] = f.readlines()
        return lines[-1].strip() if lines else "No notes yet!."
    except FileNotFoundError:
        return "No notes yet!."


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
    try:
        with open(file=note_file, mode="r") as f:
            content: str = f.read().strip()
        if not content:
            return "No notes yet!."
        return f"Summarize the following notes: {content}"
    except FileNotFoundError:
        return "No notes yet!."


# Entry point for the FastMCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
