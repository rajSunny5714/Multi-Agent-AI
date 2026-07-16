from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """
    Search the web using Tavily.
    Returns titles, URLs and snippets.
    """

    results = tavily.search(
        query=query,
        max_results=5,
        search_depth="advanced"
    )

    output = []

    for r in results["results"]:
        output.append(
            f"""
Title: {r["title"]}
URL: {r["url"]}
Snippet: {r["content"]}
"""
        )

    return "\n----------------------\n".join(output)


@tool
def scrape_url(url: str) -> str:
    """
    Scrape text from a webpage.
    """

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header"
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:5000]

    except Exception as e:
        return f"Error scraping URL : {e}"