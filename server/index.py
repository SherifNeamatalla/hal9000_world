from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware

from config.env_loader import load_env
from runner import do_load_agent, do_act, do_chat, do_create_agent, do_list_agents
from util.config_util import init_app_config

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_env()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/agent/list")
async def list_agents():
    return do_list_agents()


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


@app.post("/agent/act/{agent_id}")
async def act(agent_id: str, command: dict = Body(...)):
    return do_act(agent_id, command)


if __name__ == "__main__":
    import uvicorn

    init_app_config()

    uvicorn.run(app, host="0.0.0.0", port=8000)
