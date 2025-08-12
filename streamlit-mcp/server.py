# server.py
import os
import sys

import requests
import uvicorn
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from html2text import html2text
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.shared.exceptions import McpError
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, ErrorData
from ollama import ChatResponse, chat
from requests import Response
from requests.exceptions import RequestException
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

# Load environment variables
load_dotenv()

if os.getenv("MODEL_NAME") is None:
    raise ValueError("MODEL_NAME is not set")
    sys.exit(1)

# Get model name from environment variables
MODEL_NAME: str = os.getenv(key="MODEL_NAME", default="gpt-4.1-nano")


# MCP server instance
mcp = FastMCP(name="wiki-summary")


# Tool: Summarize wikipedia article
@mcp.tool()
async def summarize_wikipedia_article(url: str) -> str:
    """
    Fetch a Wikipedia article at the provided URL, parse it's main content,
    convert it to Markdown, and generate a summary using the llm.

    Usage:
        summarize_wikipedia_article("https://en.wikipedia.org/wiki/Model_Context_Protocol")
    """

    try:
        # URL validation
        if not url.startswith(("http", "https")):
            raise ValueError("Invalid URL: Must start with 'http://' or 'https://'")

        # Fetch HTML article content
        response: Response = requests.get(url)

        # Response status
        if response.status_code != 200:
            raise McpError(
                error=ErrorData(
                    code=INVALID_PARAMS,
                    message=f"Failed to fetch the article. Status code: {response.status_code}",
                )
            )

        # Parse HTML article content
        soup = BeautifulSoup(markup=response.text, features="html.parser")

        # Main window content text
        content_div = soup.find(name="div", attrs={"id": "mw-content-text"})
        if not content_div:
            raise McpError(
                error=ErrorData(
                    code=INVALID_PARAMS,
                    message="Failed to find the main content of the article.",
                )
            )

        # Convert HTML content to Markdown
        markdown_text: str = html2text(html=str(object=content_div))

        # Summarize the article using llm
        prompt: str = f"Summarize the following text:\n\n{markdown_text}\n\nSummary:"
        llm: ChatResponse = chat(
            model=MODEL_NAME, messages=[{"role": "user", "content": prompt}]
        )
        summary: str = llm["message"]["content"].strip()

        return summary

    except ValueError as e:
        raise McpError(
            error=ErrorData(
                code=INVALID_PARAMS,
                message=str(object=e),
            )
        ) from e

    except RequestException as e:
        raise McpError(
            error=ErrorData(
                code=INTERNAL_ERROR, message=f"Request Error: {str(object=e)}"
            )
        ) from e

    except Exception as e:
        raise McpError(
            error=ErrorData(
                code=INTERNAL_ERROR, message=f"Unexpected Error: {str(object=e)}"
            )
        ) from e


# Set up SSE transport for mcp server
sse = SseServerTransport(endpoint="/messages/")


async def sse_handler(request: Request) -> None:
    """Handle SSE connection."""
    _server = mcp._mcp_server
    async with sse.connect_sse(
        scope=request.scope, receive=request.receive, send=request._send
    ) as (reader, writer):
        await _server.run(
            read_stream=reader,
            write_stream=writer,
            initialization_options=_server.create_initialization_options(),
        )


# Create Starlette app with SSE route
app = Starlette(
    debug=True,
    routes=[
        Route(path="/sse", endpoint=sse_handler),
        Mount(path="/messages/", app=sse.handle_post_message),
    ],
)


if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8000)
