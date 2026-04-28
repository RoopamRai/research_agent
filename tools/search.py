"""Web Search Tool leveraging Tavily API."""

import os
from langchain_core.tools import tool
from tavily import TavilyClient

@tool
def web_search(query: str) -> str:
    """
    Search the web for up-to-date facts, research, and general information.
    
    Args:
        query: The topic or specific question to search for.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY is missing from environment."
        
    client = TavilyClient(api_key=api_key)
    
    # We ask for 3 results to balance finding data vs overloading Claude with text
    response = client.search(query=query, max_results=3)
    
    results = []
    # Parse the JSON response into a clean, readable string format for the LLM
    for item in response.get("results", []):
        snippet = f"Title: {item['title']}\nURL: {item['url']}\nSnippet: {item['content']}"
        results.append(snippet)
        
    return "\n---\n".join(results)
