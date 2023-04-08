import json
import sqlite3

from config.constants import HELLO_WORLD_DB_PATH
from database.db_manager_interface import IDBManager

AGENTS_TABLE = "agents"

# Create a connection to the database
conn = sqlite3.connect(HELLO_WORLD_DB_PATH)

# Create the agents table if it doesn't already exist
c = conn.cursor()
c.execute(f'''CREATE TABLE IF NOT EXISTS {AGENTS_TABLE}
             (id INTEGER PRIMARY KEY, name TEXT, role TEXT, goals TEXT, config TEXT, long_term_memory TEXT, short_term_memory TEXT)''')


class SQLite3DBManager(IDBManager):

    # Define the functions for working with the agents table
    def add(self, name, role, goals, config, long_term_memory="", short_term_memory=""):
        goals_str = json.dumps(goals)
        config_str = json.dumps(config.__dict__())
        ltm_str = json.dumps(long_term_memory)
        stm_str = json.dumps(short_term_memory)
        c.execute(
            "INSERT INTO agents (name, role, goals, config, long_term_memory, short_term_memory) VALUES (?, ?, ?, ?, ?, ?)",
            (name, role, goals_str, config_str, ltm_str, stm_str))
        conn.commit()
        agent_id = c.lastrowid
        return agent_id

    def delete(self, agent_id):
        c.execute("DELETE FROM agents WHERE id=?", (agent_id,))
        conn.commit()

    def update(self, agent_id, name=None, role=None, goals=None, config=None, long_term_memory=None,
               short_term_memory=None):
        if name:
            c.execute("UPDATE agents SET name=? WHERE id=?", (name, agent_id))
        if role:
            c.execute("UPDATE agents SET role=? WHERE id=?", (role, agent_id))
        if goals:
            goals_str = json.dumps(goals)
            c.execute("UPDATE agents SET goals=? WHERE id=?", (goals_str, agent_id))
        if config:
            config_str = json.dumps(config.__dict__())
            c.execute("UPDATE agents SET config=? WHERE id=?", (config_str, agent_id))
        if long_term_memory:
            ltm_str = json.dumps(long_term_memory)
            c.execute("UPDATE agents SET long_term_memory=? WHERE id=?", (ltm_str, agent_id))
        if short_term_memory is not None:
            stm_str = json.dumps(short_term_memory)
            c.execute("UPDATE agents SET short_term_memory=? WHERE id=?", (stm_str, agent_id))
        conn.commit()

    def get(self, agent_id):
        c.execute("SELECT * FROM agents WHERE id=?", (agent_id,))
        agent = c.fetchone()
        if agent:
            return {'id': agent[0], 'name': agent[1], 'role': agent[2], 'goals': json.loads(agent[3]),
                    'config': json.loads(agent[4]), 'long_term_memory': json.loads(agent[5]),
                    'short_term_memory': json.loads(agent[6])}
        else:
            return None

    def list(self):
        c.execute("SELECT * FROM agents")
        agents = c.fetchall()
        return [{'id': agent[0], 'name': agent[1], 'role': agent[2], 'goals': json.loads(agent[3]),
                 'config': json.loads(agent[4]), 'long_term_memory': json.loads(agent[5]),
                 'short_term_memory': json.loads(agent[6])} for agent in agents]
