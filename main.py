# Agent
"""
    A chain that knows how to use tools
    WIll take that list of tools and convert them into JSON functions description
    Still has input variable, memory, prompts, etc all the normal things a chain has
"""
# AgentExecutor
"""
    Takes an agent and runs it until the response is not a function call
    Essentially a fancy while loop
"""
# Important 
"""
The docs show several different ways of creating an Agent + AgentExecutor
They are all doing the same thing behind the scenes!
"""


from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool

load_dotenv()

chat = ChatOpenAI()
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [run_query_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools
)

agent_executor("How many users have provided a shipping address?")

# agent_executor("How many users are in the database?")