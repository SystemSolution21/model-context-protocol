"""
This module provides functionality to fetch YouTube video transcripts using the youtube_transcript_api
and exposes this functionality as a tool through the Model Context Protocol (MCP).
"""

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api._api import YouTubeTranscriptApi

from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    VideoUnavailable,
)
from youtube_transcript_api._transcripts import (
    FetchedTranscript,
    Transcript,
    TranscriptList,
)
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter

# Initialize the FastMCP server
mcp = FastMCP(name="youtube-transcripts")


# Tool: Get YouTube transcript
def get_youtube_transcript(
    video_id: str, lang_code: str = "en", format: str = "json"
) -> str:
    """
    Retrieves the transcript for a given YouTube video ID in the specified language and format.

    This function handles fetching the transcript using the youtube_transcript_api,
    formatting it, and managing potential errors like video unavailability or
    disabled transcripts.

    Args:
        video_id: The unique identifier of the YouTube video.
        lang_code: The language code for the transcript (e.g., "en", "es", "fr"). Defaults to "en".
        format: The desired output format for the transcript. Must be either "text" or "json".
                Defaults to "json".

    Returns:
        A string containing the transcript in the specified format.

    Raises:
        ValueError: If input parameters are invalid, the video is unavailable,
                    transcripts are disabled, or any other error occurs during fetching.
    """
    VALID_FORMATS: set[str] = {"text", "json"}

    # Validate input types
    if not isinstance(video_id, str):
        raise ValueError("The video_id must be a string.")
    if not isinstance(lang_code, str):
        raise ValueError("The lang_code must be a string.")
    if not isinstance(format, str) or format.lower() not in VALID_FORMATS:
        raise ValueError(f"The format must be one of {VALID_FORMATS}.")

    try:
        # Attempt to retrieve the transcript
        transcript_list: TranscriptList = YouTubeTranscriptApi.list_transcripts(
            video_id=video_id
        )
        fetched_transcript: Transcript = transcript_list.find_transcript(
            language_codes=[lang_code]
        )

        # Initialize the appropriate formatter
        transcript: FetchedTranscript = fetched_transcript.fetch()
        if format.lower() == "text":
            formatter = TextFormatter()
            return formatter.format_transcript(transcript=transcript)
        else:
            formatter = JSONFormatter()
            return formatter.format_transcript(transcript=transcript)

    except VideoUnavailable:
        raise ValueError(f"The video with ID '{video_id}' is unavailable.")
    except TranscriptsDisabled:
        raise ValueError(
            f"Transcripts are disabled for the video with ID '{video_id}'."
        )
    except Exception as e:
        raise ValueError(f"An error occurred while fetching the transcript: {e}")


# Tool: Fetch YouTube transcript
@mcp.tool()
def fetch_youtube_transcript(
    video_id: str, lang_code: str = "en", format: str = "json"
) -> str:
    """
    Tool to fetch the transcript of a YouTube video.

    :param video_id: The unique identifier of the YouTube video.
    :param lang_code: The language code for the transcript (default is 'en' for English).
    :param format: The desired output format of the transcript; either 'text' or 'json'.
    :return: The transcript in the specified format.
    """
    return get_youtube_transcript(video_id=video_id, lang_code=lang_code, format=format)


# Entry point for the FastMCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")

    # print(
    #     fetch_youtube_transcript(
    #         video_id="mWaMSGwiSB0",
    #         lang_code="en",
    #         format="text",
    #     )
    # )
