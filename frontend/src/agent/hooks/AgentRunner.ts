import { useEffect, useState } from 'react';
import { chatAgent, loadAgent } from '../../api/AgentsApiService';
import { Agent } from '../model/Agent';

export function useAgentRunner({ agentId } = {
  agentId: null,
}) {

  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [command, setCommand] = useState(null);

  useEffect(() => {
    if (!agentId) {
      return;
    }

    fetchAgent();

  }, [agentId]);


  async function fetchAgent() {
    if (!agentId) {
      return;
    }

    setLoading(true);

    try {
      const response = await loadAgent(agentId);
      const data = response.data as Agent;
      setAgent(data);
    } catch (error) {
      //TODO: handle error
    } finally {
      setLoading(false);
    }
  }

  async function chat(message?: string) {
    if (!agentId) {
      return;
    }

    const response = await chatAgent(agentId, message);

    setAgent(response.data);


  }

  return { agent, loading, error, chat, command };

}
