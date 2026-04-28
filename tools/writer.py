"""Tool for writing markdown reports to the local filesystem."""

import os
from langchain_core.tools import tool

@tool
def write_markdown_report(filename: str, content: str) -> str:
    """
    Writes the final synthesized research report to a local markdown file.
    Always call this when the research is complete to save the output.
    
    Args:
        filename: The desired name of the file (e.g., 'research_report.md').
        content: The complete markdown structured content of the report.
    """
    # Security: Ensure we only write into the current project directory
    safe_filename = os.path.basename(filename) 
    if not safe_filename.endswith(".md"):
        safe_filename = f"{safe_filename}.md"
        
    file_path = os.path.join(os.getcwd(), safe_filename)
    
    # Write using standard I/O (async would be used here in C# or Prod Python)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # The agent receives this observation so it knows the task succeeded.
    return f"Success! Report prominently saved to {file_path}"
