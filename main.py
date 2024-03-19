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
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
        )),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [
    run_query_tool,
    describe_tables_tool,
    write_report_tool
]

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
agent_executor("How many orders are there? Write the results to a html report.")

agent_executor(
    "Repeat the exact same process for users."
)

# agent_executor("Summarize the top 5 most popular products. Write the results to a report file.")

# agent_executor("How many users have provided a shipping address?")
# agent_executor("how many users are there?")
