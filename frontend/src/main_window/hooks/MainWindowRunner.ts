import { useEffect, useState } from 'react';
import { actAgent, chatAgent, listAgents, loadAgent } from '../../api/AgentsApiService';
import { Agent } from '../../agent/model/Agent';
import { AGENT_ROLE, USER_ROLE } from '../../config/Constants';
import { parseJSONWithTrailingCommas } from '../../util/json_util';
import { synthesizeSpeech } from '../../api/ElevenLabsApi';

//TODO : refactor the fuck out of this monstrosity
export function useMainWindowRunner() {
  const [showHal, setShowHal] = useState(false);

  const [agentState, setAgentState] = useState({});

  const [logs, setLogs] = useState<Array<string>>([]);

  const agents = useAgents({ setLogs });

  const {
    selectedAgent, selectedAgentId, setSelectedAgentId,
    command, goals, role, config, chatHistory,
    onSendMessage, onResendMessage, onAgentAct, audioUrl,
  } = useAgentSelected(agents, setLogs, showHal, setShowHal);



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
    onAgentAct,
    showHal,
    audioUrl,
  };
}


const useAgentSelected = (agents: Array<Agent>, setLogs: any, showHal: any, setShowHal: any) => {
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  // Agent fields
  const [goals, setGoals] = useState<Array<string>>([]);
  const [command, setCommand] = useState<string | undefined>(undefined);
  const [role, setRole] = useState<string | undefined>(undefined);
  const [config, setConfig] = useState<string | undefined>(undefined);
  const [chatHistory, setChatHistory] = useState<Array<any>>([]);
  const [thoughts, setThoughts] = useState<any>(undefined);
  const [audioUrl, setAudioUrl] = useState<string | undefined>(undefined);


  useEffect(() => {
    if (!selectedAgentId || !agents.length) {
      setSelectedAgent(null);
      return;
    }

    fetchAgent();
  }, [selectedAgentId, agents]);

  useEffect(() => {
    if (!thoughts || !thoughts?.speak) {
      setAudioUrl(undefined);
      return;
    }

    handleSynthesizeSpeech(thoughts.speak);


  }, [thoughts]);

  useEffect(() => {
    if (!selectedAgent) {
      setAudioUrl(undefined);
      setCommand(undefined);
      setGoals([]);
      setRole(undefined);
      setConfig(undefined);
      setChatHistory([]);
      return;
    }

    setAudioUrl(undefined);

    const mappedHistory = (selectedAgent.chatHistory || []).map((entry: any) => {
      // @ts-ignore
      const role = entry['role'];
      // @ts-ignore
      let content = entry['content'];
      console.debug({role,content})

      if (role === AGENT_ROLE) {
        try {
          content = parseJSONWithTrailingCommas(content);

          console.debug({ content });
          entry['content'] = content;

        } catch (e) {
          console.debug({ kek: content, e });

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

  async function handleSynthesizeSpeech(text: string) {
    const elevenLabsVoices = {
      "old_f_australian": "yb4LSSX00nWconeQQujS",
      "young_f_british": "5OBhy9rwDPoHd4oqEeDd"

    }

    try {
      const synthesizedAudioUrl = await synthesizeSpeech(text, elevenLabsVoices["young_f_british"]);
      setAudioUrl(synthesizedAudioUrl);
    } catch (error) {
      console.error('Error synthesizing speech:', error);
    }
  };


  async function fetchAgent() {
    if (!selectedAgentId) {
      return;
    }

    try {
      setShowHal(true);
      const response = await loadAgent(selectedAgentId);
      // @ts-ignore
      const data = response.data?.result as Agent;
      setSelectedAgent(data);
    } catch (error) {
      //TODO: handle error
    } finally {
      setShowHal(false);
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

    console.debug({content});
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
      setShowHal(true);
      const response = await chatAgent(selectedAgentId, message);

      // @ts-ignore
      const data = response.data?.result;
      const agent = data.agent as Agent;
      const command = data.command as string;
      // @ts-ignore
      const logs = response.data?.logs as Array<string>;

      setSelectedAgent(agent);
      setCommand(parseJSONWithTrailingCommas(command));
      setLogs(logs);

    } catch (error) {
      // @ts-ignore
      newEntry['confirmed'] = 'error';
      setChatHistory([...chatHistory]);
    } finally {
      setShowHal(false);
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

  async function onAgentAct(userInput: string) {
    if (!selectedAgentId) {
      return { 'status': 'error', 'message': 'No agent found!' };
    }

    if (!command) {
      return { 'status': 'error', 'message': 'No command found!' };
    }
    // @ts-ignore
    try {
      setShowHal(true);
      const response = await actAgent(selectedAgentId, userInput, command);
      // @ts-ignore
      const data = response.data;
      const agent = data.result as Agent;
      // @ts-ignore
      const logs = response.data?.logs as Array<string>;

      setSelectedAgent(agent);
      setLogs(logs);
    } catch (error) {
    } finally {
      setShowHal(false);
    }

  }

  return {
    selectedAgent, selectedAgentId, setSelectedAgentId,
    command, goals, role, config, chatHistory, thoughts,
    onSendMessage, onResendMessage, onAgentAct, audioUrl,
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
