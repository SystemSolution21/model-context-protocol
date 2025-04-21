import asyncio
import sys
import traceback
from typing import Any
from urllib.parse import urlparse

from mcp import ClientSession
from mcp.client.sse import sse_client


def print_items(name: str, result: Any) -> None:
    """
    Print items from the result.
    """
    print(f"\nAvailable {name}:")

    items = getattr(result, name)

    if items:
        for item in items:
            print(" *", item)
    else:
        print(f"No items available.")


async def main(server_url: str, article_url: str) -> None:
    """
    Connect to the MCP server and call the summarize_wikipedia_article tool.

    Args:
        server_url: Full URL to SSE endpoint (e.g. http://localhost:8000/sse)
        article_url: Wikipedia URL to fetch and summarize
    """

    if urlparse(url=server_url).scheme not in ("http", "https"):
        raise ValueError("Invalid server URL. Must start with 'http://' or 'https://'")

    try:
        async with sse_client(url=server_url) as stream:
            async with ClientSession(
                read_stream=stream[0], write_stream=stream[1]
            ) as session:
                await session.initialize()
                print(f"Connected to MCP server at {server_url}.")
                print_items(name="tools", result=await session.list_tools())
                print_items(name="resources", result=await session.list_resources())
                print_items(name="prompts", result=await session.list_prompts())

                print(f'\nCalling "summarize_wikipedia_article" tool...')

                response = await session.call_tool(
                    name="summarize_wikipedia_article",
                    arguments={"url": article_url},
                )

                print("\n=== Summarized Wikipedia Article ===\n")
                print(response)

    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        traceback.print_exception(type(e), value=e, tb=e.__traceback__)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: uv run -- client.py <server_url> <wikipedia_article_url>\n"
            "Example: uv run -- client.py http://localhost:8000/sse https://en.wikipedia.org/wiki/Python_(programming_language)\n"
        )
        sys.exit(1)

    server_url: str = sys.argv[1]
    article_url: str = sys.argv[2]

    asyncio.run(
        main=main(
            server_url=server_url,
            article_url=article_url,
        )
    )
