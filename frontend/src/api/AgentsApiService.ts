import { Agent } from '../agent/model/Agent';
import { axiosInstance } from './Axios';

export function listAgents() {
  return axiosInstance.get<Agent[]>('/agent/list');
}

export function createAgent(name: string, role: string, goals: string[], config: any) {
  return axiosInstance.post<Agent>('/agent/create', { name, role, goals, config });
}

export function loadAgent(agentId: string) {
  return axiosInstance.get<Agent>(`/agent/load/${agentId}`);
}

export function chatAgent(agentId: string, message?: string) {
  return axiosInstance.post<Agent>(`/agent/chat/${agentId}`, message);
}


export function actAgent(agentId: string, commandResponse: string, command: any) {
  return axiosInstance.post(`/agent/act/${agentId}`, {
    command_response: commandResponse,
    command: command,
  });
}

export function resetAgentShortMemory(agentId: string) {
  return axiosInstance.post(`/agent/reset/${agentId}`);
}
