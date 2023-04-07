import json
import sqlite3

from fastapi import HTTPException

HELLO_WORLD_DB = "hello_world.sqlite"
AGENTS_TABLE = "agents"

# Create a connection to the database
conn = sqlite3.connect(HELLO_WORLD_DB)

# Create the agents table if it doesn't already exist
c = conn.cursor()
c.execute(f'''CREATE TABLE IF NOT EXISTS {AGENTS_TABLE}
             (id INTEGER PRIMARY KEY, name TEXT UNIQUE, role TEXT, goals TEXT)''')


# Define the functions for working with the agents table
def db_add_agent(name, role, goals):
    goals_str = json.dumps(goals)
    c.execute("INSERT INTO agents (name, role, goals) VALUES (?, ?, ?)", (name, role, goals_str))
    conn.commit()


def db_delete_agent(agent_id):
    c.execute("DELETE FROM agents WHERE id=?", (agent_id,))
    conn.commit()


def db_update_agent(agent_id, role=None, goals=None):
    if role:
        c.execute("UPDATE agents SET role=? WHERE id=?", (role, agent_id))
    if goals:
        goals_str = json.dumps(goals)
        c.execute("UPDATE agents SET goals=? WHERE id=?", (goals_str, agent_id))
    conn.commit()


def db_get_agent(agent_id):
    c.execute("SELECT * FROM agents WHERE id=?", (agent_id,))
    agent = c.fetchone()
    if agent:
        return {'id': agent[0], 'name': agent[1], 'role': agent[2], 'goals': json.loads(agent[3])}
    else:
        return None


def db_list_agents():
    c.execute("SELECT * FROM agents")
    agents = c.fetchall()
    return [{'id': agent[0], 'name': agent[1], 'role': agent[2], 'goals': json.loads(agent[3])} for agent in agents]
