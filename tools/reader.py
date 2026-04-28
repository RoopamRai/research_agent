"""Scrapes readable text from a webpage using BeautifulSoup."""

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

@tool
def read_webpage(url: str) -> str:
    """
    Extracts readable text content from a given URL.
    Use this ONLY when a search snippet lacks necessary depth.
    
    Args:
        url: The web URL to scrape.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Strip out noisy, non-content elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        text = soup.get_text(separator="\n", strip=True)
        
        # Agentic constraint: Hard cutoff to prevent Context Overflow errors
        max_length = 4000
        if len(text) > max_length:
            return f"{text[:max_length]}...\n\n[CONTENT TRUNCATED]"
            
        return text
    except Exception as e:
        # We return the error as text so the Agent knows it failed and can adapt!
        return f"Error reading page {url}: {str(e)}"
