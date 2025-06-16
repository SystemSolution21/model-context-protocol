import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient


# Load environment variables from .env file
load_dotenv()

# Define the path to the configuration file
config_path: Path = Path(__file__).parent / "browser_mcp.json"

# Create MCPClient from config file
mcp_client: MCPClient = MCPClient(config=str(object=config_path))

# Create llm
llm: ChatOllama = ChatOllama(model="llama3.2:3b")

# Create agent with the client
mcp_agent: MCPAgent = MCPAgent(llm=llm, client=mcp_client, max_steps=30)


# Define the query
query = "Find the best restaurant in Tokyo USING GOOGLE SEARCH"


# Run the query
async def main() -> None:
    response = await mcp_agent.run(
        query=query,
        max_steps=30,
    )
    print(f"\nSearch Result: {response}")


if __name__ == "__main__":
    asyncio.run(main())
