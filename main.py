#from currentsapi import CurrentsAPI
import httpx
from mcp.server.fastmcp import FastMCP
import mcp.types as types
import requests
from os import environ
from typing import Any, Optional

mcp = FastMCP("getnews_app")


API_KEY = environ.get('CURRENTSNEWS_API_KEY')
if not API_KEY:
    raise ValueError("API key for Currents News API is not set in environment variables.")

USER_AGENT = "getnews_app/1.0"

PROMPTS = {
    "get-news": types.Prompt(
        name="get-news",
        description="Get latest news",
        arguments=[
            types.PromptArgument(
                name="changes",
                description="Git diff or description of changes",
                required=True
            )
        ],
    ),
}


async def make_currentsnew_api_request(url: str, params: dict=None) -> dict[str, Any] | None:
    """Make a request to the lastfm with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()

            return response.json()
        
        except Exception:
            return None

@mcp.tool()
async def get_latest_news(language: Optional[str] = "en", api_key: str = None) -> dict:
    """
    Retrieves the latest news from the Currents News API.

    Args:
        language: Filter news by language code.
            Valid Values: Supported language codes are available via /v1/available/languages.
                or get_languages()
            Default: "en" (English)
        api_key: Your Currents News API key.  Required.

    Returns:
        A dictionary containing the JSON response from the API.  Returns an empty dictionary
        if the API key is missing or if an error occurs.
    """
    url = "https://api.currentsapi.services/v1/latest-news"
    params = {}

    if api_key is None:
        print("Error: api_key is a required parameter.")
        return {}  # Return an empty dictionary to indicate an error

    params["language"] = language
    params["apiKey"] = api_key # Include api_key in the parameters

    return await make_currentsnew_api_request(url, params=params)

@mcp.tool()
async def news_search(
    language: Optional[str] = "en",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    type: Optional[int] = 1,
    country: Optional[str] = "INT",
    category: Optional[str] = None,
    page_number: Optional[int] = 1,
    domain: Optional[str] = None,
    domain_not: Optional[str] = None,
    keywords: Optional[str] = None,
    page_size: Optional[int] = 30,
    limit: Optional[int] = None,
) -> dict:
    """
    Wraps the Currents News API search endpoint to retrieve news articles.
    Args:
        language: Filter results by language code.
            Valid Values: Codes available via /v1/available/languages. Default: en (English)
            or get_languages()
        start_date: Search for news published after the given date.
            Default: Current UTC time. Format: RFC 3339 format (e.g., "2023-10-26T10:00:00.000Z")
        end_date: Search for news published before the given date.
            Default: Current UTC time. Format: RFC 3339 format
        type: Filter results by content type.
            Valid Values: 1 (news), 2 (articles), 3 (discussion content). Default: 1
        country: Filter by the country code of the news source.
            Valid Values: Codes available via the /v1/available/regions endpoint. Default: INT (International)
            or get_regions()
        category: Filter results by news category.
            Valid Values: Categories available via /v1/available/categories
            or get_categories()
        page_number: The page number to access older results.
            Valid Values: Any integer greater than zero. Default: 1
        domain: Filter results by specific website domains.
            Format: Primary domain name without prefixes (e.g., example.com)
        domain_not: Exclude specific domains from results.
            Format: Primary domain name without prefixes
        keywords: Search for exact matches of words in titles or descriptions.
            Format: String
        page_size: Specify the number of articles per page.
            Valid Values: Any integer between 1 and 200. Default: 30
        limit: Specify the total number of articles returned.
            Valid Values: Any integer between 1 and 200. Default: Returns all matching articles
    Returns:
        A dictionary containing the JSON response from the API. Returns an empty dictionary
        if the API key is missing or if an error occurs.
    """
    url = "https://api.currentsapi.services/v1/search"
    params = {}

    params['apiKey'] = API_KEY # Use the API_KEY constant

    if language:
        params["language"] = language
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if type:
        params["type"] = type
    if country:
        params["country"] = country
    if category:
        params["category"] = category
    if page_number:
        params["page_number"] = page_number
    if domain:
        params["domain"] = domain
    if domain_not:
        params["domain_not"] = domain_not
    if keywords:
        params["keywords"] = keywords
    if page_size:
        params["page_size"] = page_size
    if limit:
        params["limit"] = limit

    return await make_currentsnew_api_request(url, params=params)

@mcp.tool()
async def get_categories() -> dict:
    """
    Wraps the Currents News API endpoint to retrieve available news categories.
    Args:
    Returns:
        A dictionary containing the JSON response from the API. Returns an empty dictionary
        if the API key is missing or if an error occurs.
    """
    url = "https://api.currentsapi.services/v1/available/categories"
    params = {}

    params['apiKey'] = API_KEY

    return await make_currentsnew_api_request(url, params=params)


@mcp.tool()
async def get_regions() -> dict:
    """
    Wraps the Currents News API endpoint to retrieve supported country codes (regions).
    Args:
    Returns:
        A dictionary containing the JSON response from the API. Returns an empty dictionary
        if the API key is missing or if an error occurs.
    """
    url = "https://api.currentsapi.services/v1/available/regions"
    params = {}

    params['apiKey'] = API_KEY
    return await make_currentsnew_api_request(url, params=params)

@mcp.tool()
async def get_languages() -> dict:
    """
    Wraps the Currents News API endpoint to retrieve supported languages.
    Args:
    Returns:
        A dictionary containing the JSON response from the API. Returns an empty dictionary
        if the API key is missing or if an error occurs.
    """
    url = "https://api.currentsapi.services/v1/available/languages"
    params = {}

    params['apiKey'] = API_KEY
    return await make_currentsnew_api_request(url, params=params)
