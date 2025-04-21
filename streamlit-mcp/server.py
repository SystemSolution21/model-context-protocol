# server.py
import requests
from requests import Response
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from html2text import html2text

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount

from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from mcp.server.sse import SseServerTransport

from ollama import chat, ChatResponse

# Create mcp server instance
mcp = FastMCP(name="wiki-summary")


# Tool: Get summary from wikipedia
@mcp.tool()
async def summarize_wikipedia_article(url: str):
    """
    Fetch a Wikipedia article at the provided URL, parse its main content,
    convert it to Markdown, and generate a summary using the llm.

    Usage:
        summarize_wikipedia_article("https://en.wikipedia.org/wiki/Python_(programming_language)")
    """

    try:
        # validate url
        if not url.startswith(("http", "https")):
            raise ValueError("Invalid URL: Must start with 'http://' or 'https://'")

        # Fetch the HTML content of the Wikipedia article
        response: Response = requests.get(url)

        # Check response status
        if response.status_code != 200:
            raise McpError(
                error=ErrorData(
                    code=INVALID_PARAMS,
                    message=f"Failed to fetch the article. Status code: {response.status_code}",
                )
            )

        # Parse the HTML content of article
        soup = BeautifulSoup(markup=response.text, features="html.parser")

        # Find the main content of the article
        content_div = soup.find(name="div", attrs={"id": "mw-content-text"})
        if not content_div:
            raise McpError(
                error=ErrorData(
                    code=INVALID_PARAMS,
                    message="Failed to find the main content of the article.",
                )
            )

        # Convert the HTML content to Markdown
        markdown_text: str = html2text(html=str(object=content_div))

        # Generate a summary using llm
        prompt: str = f"Summarize the following text:\n\n{markdown_text}\n\nSummary:"
        llm: ChatResponse = chat(
            model="gemma3.2:3b", messages=[{"role": "user", "content": prompt}]
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
sse = SseServerTransport("/messages/")


async def sse_handler(request: Request):
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
