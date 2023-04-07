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


@app.get("/agent/load")
async def load_agent(name: str):
    return do_load_agent(name)


@app.post("/agent/chat")
async def chat(name: str, message: str = Body(...)):
    return do_chat(name, message)


@app.post("/agent/act")
async def act(name: str):
    return do_act(name)


@app.post("/agent/wake")
async def wake(name: str):
    return do_wake(name)


if __name__ == "__main__":
    import uvicorn

    AppConfig()

    uvicorn.run(app, host="0.0.0.0", port=8000)
