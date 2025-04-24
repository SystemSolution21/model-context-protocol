# Streamlit MCP

This is a Streamlit app that allows you to interact with custom Model Context Protocol (MCP) servers.

## Features

- **Streamlit Web Interface:**  
  Provides a simple web UI for users to interact with MCP servers.

- **MCP Server Communication:**  
  Connects to an MCP server using Server-Sent Events (SSE) for real-time communication.

- **Wikipedia Article Summarization:**  
  Allows users to input a Wikipedia article URL and receive a summarized version of the article using the `summarize_wikipedia_article` tool provided by the MCP server.

- **Error Handling:**  
  Displays clear error messages if the server is unreachable or if the summarization fails.

## Functionality

- Enter the MCP server SSE URL and a Wikipedia article URL in the Streamlit app.
- On clicking "Fetch and Summarize", the app:
  - Connects to the specified MCP server via SSE.
  - Calls the `summarize_wikipedia_article` tool on the server with the provided article URL.
  - Displays the summarized article in the web interface.

## Files

- `app.py`: Main Streamlit client application.
- `client.py`: Command-line client for interacting with the MCP server.
- `server.py`: Example MCP server implementation with a Wikipedia summarization tool.

## Usage

1. **Start the MCP server:**
   python server.py

2. **Run the Streamlit app:**
   streamlit run app.py

Open the app in browser, enter the server URL (default: `http://localhost:8000/sse`) and a Wikipedia article URL, then click "Fetch and Summarize".
