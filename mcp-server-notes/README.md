# mcp-server-notes

A simple MCP (Model Context Protocol) server that allows you to add, read, and summarize notes.

It uses the FastMCP library to provide a standardized interface for interacting with the notes.

Features:

- Add notes
- Read notes
- Summarize notes

Requirements:

- Python 3.8+
- mcp[cli]

Run:

- mcp dev notes.py # Executes the server on Localhost:6274 MCP Inspector v0.9.0
- mcp install notes.py # Executes the server locally on Claude Desktop
