# mcp-server-pokemon

A simple MCP (Model Context Protocol) server that connects to the Pokemon API and exposes tools that an LLM can use to fetch Pokemon data, list popular Pokemon, and build a tournament squad.

It uses the FastMCP library and HTTPX to fetch live Pokemon info via a standardized protocol that works seamlessly with LLMs and AI agents.

Features:

- Get detailed info about any Pokemon
- Create a powerful tournament squad
- List popular Pokemon picks

Requirements:

- Python 3.8+
- Node.js (for some LLM hosts that require it)
- HTTPX
- mcp[cli]

Run:

- mcp dev pokemon.py # Executes the server on Localhost:6274 MCP Inspector v0.16.3
- mcp install pokemon.py # Executes the server locally on Claude Desktop
