"""Entry point for the Research Assistant Agent."""

import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# 1. Load environment variables (API Keys) from .env FIRST
# This must happen before importing the LLM so it has the keys.
load_dotenv()

from agent.graph import app

def run_agent(query: str):
    """
    Kicks off the LangGraph execution and streams the ReAct loop to the console.
    """
    print(f"\n🚀 Starting Agentic Research on: '{query}'\n")
    print("-" * 50)
    
    # 2. Initialize the State with the very first Human Message
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # 3. Stream the graph updates
    # This exposes the Perceive -> Reason -> Act loop live!
    for output in app.stream(inputs, stream_mode="updates"):
        
        # output is a dict mapping \{node_name : state_update\}
        for node_name, state_update in output.items():
            print(f"\n[ Node Finished: {node_name.upper()} ]")
            
            # Extract the raw message that was just appended to the state
            latest_message = state_update["messages"][-1]
            
            # Print the Agent's reasoning (Thought)
            if latest_message.content:
                print(f"Thought/Response: {latest_message.content}")
                
            # If the Agent decided to call tools (Action), display its intent
            if hasattr(latest_message, 'tool_calls') and latest_message.tool_calls:
                for tool_call in latest_message.tool_calls:
                    print(f"🛠️  Action: Calling '{tool_call['name']}' with args: {tool_call['args']}")
    
    print("\n" + "-" * 50)
    print("✅ Agent Execution Complete.")

if __name__ == "__main__":
    # Allow running via CLI args (e.g., python main.py "What is LangGraph?")
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        # Fallback to interactive input
        user_query = input("Enter a research topic: ")
        
    run_agent(user_query)
