# import packages
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor, initialize_agent
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv

import chainlit as cl

from tools.sql import run_query_tool, list_tables, describe_tables_tool

# load_dotenv()


# get list of tables
tables = list_tables()

@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate(
        messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )


    # intialised memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    tools = [
        run_query_tool,
        describe_tables_tool
    ]

    agent = initialize_agent(
        llm=model,
        prompt=prompt,
        tools=tools,
        memory=memory
    )

    # agent_executor = AgentExecutor(
    #     agent=agent,
    #     verbose=True,
    #     tools=tools,
    #     memory=memory
    # )

    # runnable = prompt | model | StrOutputParser() | agent
    cl.user_session.set("agent", agent)

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)
    await cl.make_async(agent.run)(message.content, callbacks=[cb])