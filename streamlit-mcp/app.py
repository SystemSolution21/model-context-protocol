import asyncio
import traceback
from typing import Any

import streamlit as st
from mcp import ClientSession
from mcp.client.sse import sse_client


async def call_tool(server_url: str, article_url: str) -> Any:
    """
    Connects to the MCP server using SSE, initializes the session,
    calls the summarize_wikipedia_article tool, and returns the result.
    """

    try:
        async with sse_client(url=server_url) as stream:
            async with ClientSession(
                read_stream=stream[0], write_stream=stream[1]
            ) as session:
                await session.initialize()
                response = await session.call_tool(
                    name="summarize_wikipedia_article",
                    arguments={"url": article_url},
                )
                return response

    except Exception as e:
        return f"Error: {e}\n{traceback.format_exc()}"


async def main() -> None:
    st.set_page_config(page_title="Streamlit-MCP-Client")
    st.title(body="Streamlit as a MCP Client")
    st.markdown(
        body="""Enter the "MCP Server SSE URL" and a "Wikipedia Article URL" to fetch and summarize the article:"""
    )

    server_url: str = st.text_input(
        label="MCP Server URL", value="http://localhost:8000/sse"
    )
    article_url: str = st.text_input(
        label="Wikipedia Article URL",
        value="https://en.wikipedia.org/wiki/Model_Context_Protocol",
    )

    if st.button(label="Fetch and Summarize"):
        with st.spinner(text="Fetching and summarizing the article..."):
            try:
                response = await call_tool(
                    server_url=server_url, article_url=article_url
                )
                result: str = response.content[0].text

                st.subheader(body="Article Summary:")
                st.markdown(body=result)

            except Exception as e:
                st.error(body=f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main=main())
