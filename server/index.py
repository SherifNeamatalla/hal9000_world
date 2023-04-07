import json

from fastapi import FastAPI, Body

from commands.cmd_interface import ICmd
from config.app_config import AppConfig
from config.env_loader import load_env
from runner import do_load_agent, do_wake, do_act, do_chat, do_create_agent

app = FastAPI()

load_env()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Define the endpoint for your service
@app.post("/agent/create")
async def create_agent(name: str, role: str, goals: list, config: dict):
    return do_create_agent(name, role, goals, config)


@app.get("/agent/load/{agent_id}")
async def load_agent(agent_id: str):
    return do_load_agent(agent_id)


@app.post("/agent/chat/{agent_id}")
async def chat(agent_id: str, message: str = Body(...)):
    return do_chat(agent_id, message)

# Does chat & act
@app.post("/agent/loop/{agent_id}")
async def chat(agent_id: str, message: str = Body(...)):
    return do_loop(agent_id, message)

@app.post("/agent/act/{agent_id}")
async def act(agent_id: str, command: dict = Body(...)):
    return do_act(agent_id, command)


@app.post("/agent/wake")
async def wake(name: str):
    return do_wake(name)


if __name__ == "__main__":
    import uvicorn

    AppConfig()

    uvicorn.run(app, host="0.0.0.0", port=8000)
