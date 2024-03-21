import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite", check_same_thread=False)

def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"

class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema= RunQueryArgsSchema
)

class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]

def describe_tables(tables_names):
    c = conn.cursor()
    tables = ', '.join("'" + table + "'" for table in tables_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of tables names, returns the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)