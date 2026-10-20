from tavily import TavilyClient
from dotenv import load_dotenv
from langchain.tools import tool
from typing import Dict, Any
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

load_dotenv()

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """tool to search the web for information"""
    logging.info(f"searching for {query}")
    return tavily_client.search(query)