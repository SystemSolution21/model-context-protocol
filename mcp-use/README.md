# MCP-Use

MCP-Use is the open source way to connect any LLM to any MCP server and build custom agents that have tool access, without using closed source or application clients.

Features:

- Ease of use:
  Can create MCP capable agent only few lines of code.

- LLM Flexibility:
  Works with any langchain supported LLM that supports tool calling (OpenAI, Anthropic, Groq, LLama etc.)

- HTTP Support:
  Direct connection to MCP servers running on specific HTTP ports.

- Dynamic Server Selection:
  Agents can dynamically choose the most appropriate MCP server for a given task from the available tool.

- Multi-Server Support:
  Use multiple MCP servers simultaneously in a single agent.

- Tool Restrictions:
  Restrict potentially dangerous tools like file system or network access.

- Custom Agents:
  Build own agents with any framework using the LangChain adapter or create new adapters.
