from fastapi import FastAPI
from agent import run_agent

app = FastAPI()

@app.get("/ai")
def ai(q: str):
    return {"result": run_agent(q)}