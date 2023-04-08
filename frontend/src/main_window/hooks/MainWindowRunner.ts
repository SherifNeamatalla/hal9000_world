import { useEffect, useState } from 'react';
import { chatAgent, listAgents, loadAgent } from '../../api/AgentsApiService';
import { Agent } from '../../agent/model/Agent';
import { AGENT_ROLE, USER_ROLE } from '../../config/Constants';

//TODO : refactor the fuck out of this monstrosity
export function useMainWindowRunner() {
  const [agentState, setAgentState] = useState({});

  const [logs, setLogs] = useState<Array<string>>([]);

  const agents = useAgents({ setLogs });

  const {
    selectedAgent, selectedAgentId, setSelectedAgentId,
    command, goals, role, config, chatHistory,
    onSendMessage, onResendMessage, onAgentAct,
  } = useAgentSelected(agents, setLogs);


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
    onSendMessage,
    onResendMessage,
    onAgentAct
  };
}


const useAgentSelected = (agents: Array<Agent>, setLogs: any) => {
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  // Agent fields
  const [goals, setGoals] = useState<Array<string>>([]);
  const [command, setCommand] = useState<string | undefined>(undefined);
  const [role, setRole] = useState<string | undefined>(undefined);
  const [config, setConfig] = useState<string | undefined>(undefined);
  const [chatHistory, setChatHistory] = useState<Array<any>>([]);
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


    setGoals(selectedAgent.goals);
    setRole(selectedAgent.role);
    setConfig(selectedAgent.config);
    setChatHistory(mappedHistory);
    setCommandFromHistory(mappedHistory);

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
    const content = lastMessage?.['content'];

    setCommand(content?.['command']);
    setThoughts(content?.['thoughts']);


  }

  async function onSendMessage(message?: string, isResend = false) {
    if (!message || !selectedAgentId) {
      return { 'status': 'error', 'message': 'No message or agent found!' };
    }


    let newEntry = {
      'role': USER_ROLE,
      'content': message,
      'confirmed': 'pending',
    };
    // Add message to chat history only if it is not a resend, otherwise it was already added
    if (!isResend) {
      chatHistory.push(newEntry);

      setChatHistory([...chatHistory]);

      newEntry = chatHistory[chatHistory.length - 1];
    }


    try {
      const response = await chatAgent(selectedAgentId, message);

      // @ts-ignore
      const data = response.data?.result;
      const agent = data.agent as Agent;
      const command = data.command as string;
      // @ts-ignore
      const logs = response.data?.logs as Array<string>;

      setSelectedAgent(agent);
      setCommand(command);
      setLogs(logs);
    } catch (error) {
      // @ts-ignore
      newEntry['confirmed'] = 'error';
      setChatHistory([...chatHistory]);
    }

  }

  async function onResendMessage() {
    if (!selectedAgentId || !chatHistory.length) {
      return { 'status': 'error', 'message': 'No agent found!' };
    }
    // find this  const newEntry = {
    //   'role': USER_ROLE,
    //   'content': message,
    //   'confirmed': 'pending',
    // }

    // and resend it

    const lastMessage = chatHistory[chatHistory.length - 1];

    console.debug({ lastMessage });
    if (lastMessage['role'] !== USER_ROLE || lastMessage['confirmed'] !== 'error') {
      return;
    }

    // @ts-ignore
    onSendMessage(lastMessage['content'], true);

  }

  function onAgentAct(userInput:string){

  }
  return {
    selectedAgent, selectedAgentId, setSelectedAgentId,
    command, goals, role, config, chatHistory, thoughts,
    onSendMessage, onResendMessage,onAgentAct
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
