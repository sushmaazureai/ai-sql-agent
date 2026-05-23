from mcp.server.fastapi import FastAPIMCP
from agent import run_agent

app = FastAPIMCP("sql-agent")

@app.tool()
def sql_restore(command: str) -> str:
    """
    Executes SQL restore commands using natural language
    Example:
    - restore database TestDB from C:\\backup\\test.bak
    - restore latest to TestDB
    """
    return run_agent(command)