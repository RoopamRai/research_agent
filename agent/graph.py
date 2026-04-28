"""Orchestrates the ReAct Agent loop using LangGraph."""

from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

from agent.prompts import SYSTEM_PROMPT
from tools.search import web_search
from tools.reader import read_webpage
from tools.writer import write_markdown_report

# All three tools the agent can use
tools = [web_search, read_webpage, write_markdown_report]

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)

# create_react_agent wires the full ReAct loop automatically:
#   agent node → tool node → agent node → ... → END
app = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
)
