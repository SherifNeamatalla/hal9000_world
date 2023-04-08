import { useEffect, useState } from 'react';
import { listAgents, loadAgent } from '../../api/AgentsApiService';
import { Agent } from '../../agent/model/Agent';
import { AGENT_ROLE } from '../../config/Constants';

export function useMainWindowRunner() {
  const [agentState, setAgentState] = useState({});

  const [logs, setLogs] = useState<Array<string>>([]);

  const agents = useAgents({ setLogs });

  const {
    selectedAgent, selectedAgentId, setSelectedAgentId,
    command, goals, role, config, chatHistory,
  } = useAgentSelected(agents);


  return {
    agentState,
    setAgentState,
    selectedAgentId,
    setSelectedAgentId,
    agents,
    logs,
    selectedAgent,
    command,
    goals,
    role,
    config,
    chatHistory,
  };
}


const useAgentSelected = (agents: Array<Agent>) => {
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  // Agent fields
  const [goals, setGoals] = useState<Array<string>>([]);
  const [command, setCommand] = useState<string | undefined>(undefined);
  const [role, setRole] = useState<string | undefined>(undefined);
  const [config, setConfig] = useState<string | undefined>(undefined);
  const [chatHistory, setChatHistory] = useState<string | undefined>(undefined);
  const [thoughts, setThoughts] = useState<string | undefined>(undefined);
  useEffect(() => {
    if (!selectedAgentId || !agents.length) {
      setSelectedAgent(null);
      return;
    }

    fetchAgent();
  }, [selectedAgentId, agents]);


  useEffect(() => {
    if (!selectedAgent) {
      return;
    }


    // @ts-ignore
    // const newChatHistory = JSON.parse(selectedAgent.chatHistory);


    console.debug({ newChatHistory: selectedAgent.chatHistory, selectedAgent });

    const mappedHistory = (selectedAgent.chatHistory || []).map((entry: any) => {
      // @ts-ignore
      const role = entry['role'];
      // @ts-ignore
      let content = entry['content'];

      if (role === AGENT_ROLE) {
        try {
          content = JSON.parse(entry?.content?.replace(/\n/g, ''));
          entry['content'] = content;

        } catch (e) {
          console.debug('Failed to parse command');
        }
      }

      return entry;
    });


    console.debug({mappedHistory});
    setGoals(selectedAgent.goals);
    setRole(selectedAgent.role);
    setConfig(selectedAgent.config);
    setChatHistory(mappedHistory);
    // setCommandFromHistory(newChatHistory);

  }, [selectedAgent]);


  async function fetchAgent() {
    if (!selectedAgentId) {
      return;
    }

    try {
      const response = await loadAgent(selectedAgentId);
      // @ts-ignore
      const data = response.data?.result as Agent;
      setSelectedAgent(data);
    } catch (error) {
      //TODO: handle error
    }
  }

  function setCommandFromHistory(messages: []) {
    if (!messages.length) {
      setCommand(undefined);
      return;
    }

    const lastMessage = messages[messages.length - 1];

    if (lastMessage['role'] !== AGENT_ROLE) {
      setCommand(undefined);
    }
    // @ts-ignore
    const content = lastMessage?.['content']?.replaceAll(/\n/g, '');

    setCommand(content?.['command']);
    setThoughts(content?.['thoughts']);


  }

  return {
    selectedAgent, selectedAgentId, setSelectedAgentId,
    command, goals, role, config, chatHistory, thoughts,
  };
};


// @ts-ignore
function useAgents({ setLogs }) {
  const [agents, setAgents] = useState<Array<Agent>>([]);

  useEffect(() => {
    async function fetchAgents() {
      // Axios response
      const response = await listAgents();
      const data = response.data;
      // @ts-ignore
      const agents = data['result'] as Array<Agent>;
      // @ts-ignore
      const logs = data['logs'] as Array<string>;
      // @ts-ignore
      setAgents(agents);
      setLogs(logs);
    }

    fetchAgents();
  }, []);

  return agents;
}
