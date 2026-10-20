from tavily import TavilyClient
from dotenv import load_dotenv
from langchain.tools import tool
from typing import Dict, Any
import logging

load_dotenv()

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for recipes. Include the main ingredients in the query."""
    logging.info(f"searching for {query}")
    return tavily_client.search(query, max_results=5)
