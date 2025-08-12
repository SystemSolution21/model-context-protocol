# mcp-server-notes

A simple MCP (Model Context Protocol) server that allows to add, read, and summarize notes.

It uses the FastMCP library to provide a standardized interface for interacting with the notes.

## Features

- Add notes
- Read notes
- Summarize notes

## Requirements

- Python 3.13+
- mcp[cli]

## Run

```pwsh
- mcp dev notes.py # Proxy server listening on Localhost:6277(mcp server). 
# MCP Inspector v0.16.3 is up and running at http://localhost:6274(mcp client)
- mcp install notes.py # Executes the server locally on installed Claude Desktop
```
