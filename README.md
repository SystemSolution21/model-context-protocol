# mcp-server-airbnb

This is a Gradio web interface for an Airbnb search agent using AI.

dependencies:
"gradio>=5.23.3",
"ollama>=0.4.7",
"praisonaiagents[llm]>=0.0.72"

# mcp-server-pokemon

A simple MCP (Model Context Protocol) server that connects to the PokéAPI and exposes tools that an LLM can use to fetch Pokémon data, list popular Pokémon, and build a tournament squad.

It uses the FastMCP library and httpx to fetch live Pokémon info via a standardized protocol that works seamlessly with LLMs and AI agents.

Features:
Get detailed info about any Pokémon
Create a powerful tournament squad
List popular Pokémon picks

Requirements:
Python 3.8+
Node.js (for some LLM hosts that require it)
httpx
mcp[cli]

Run:
mcp dev pokemon.py # Executes the server on Localhost:6274 MCP Inspector v0.9.0
mcp install pokemon.py # Executes the server locally on Claude Desktop
