#from currentsapi import CurrentsAPI
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
import requests
from os import environ

mcp = FastMCP("getnews_app")


API_KEY = environ.get('CURRENTSNEWS_API_KEY')
if not API_KEY:
    raise ValueError("API key for Currents News API is not set in environment variables.")

USER_AGENT = "getnews_app/1.0"


async def make_currentsnew_api_request(url: str) -> dict[str, Any] | None:
    """Make a request to the lastfm with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()

            return response.json()
        
        except Exception:
            return None

@mcp.tool()
async def get_latest_news() -> Any:
    """
    Get latest news in english
    """
    LATEST_NEWS_ENDPOINT_URL = 'https://api.currentsapi.services/v1/latest-news?' \
        'language=en&' \
        f'apiKey={API_KEY}'

    latest_news = await make_currentsnew_api_request(LATEST_NEWS_ENDPOINT_URL)

    return latest_news

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')