import React, { useEffect, useState } from 'react';
import { listAgents } from '../api/AgentsApiService';
import { Agent } from './model/Agent';
import { ListItemText } from '@material-ui/core';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { ListItemButton, ListItemIcon } from '@mui/material';
import { styled } from '@mui/system';

const AnimatedSmartToyIcon = styled(SmartToyIcon)(({ theme }) => ({
  transition: 'transform 1s linear',
  animation: 'rotate 10s linear infinite',
  '@keyframes rotate': {
    '0%': {
      transform: 'rotate(0deg)',
    },
    '100%': {
      transform: 'rotate(360deg)',
    },
  },
}));

const AgentsListContainer = styled('div')(({ theme }) => ({
  height: '100%',
  backgroundColor: theme.palette.agentsList.background,
  borderRadius: '10px',
}));

const ListContainer = styled('div')(({ theme }) => ({
  height: '100%',
  backgroundColor: theme.palette.agentsList.background,
  color: theme.palette.primary.contrastText,
  padding: theme.spacing(2),
  borderRadius: '10px',
}));

const ListItemContainer = styled('div')(({ theme }) => ({
  borderRadius: '10px',
  margin: theme.spacing(1, 0),
  '&:hover': {
    backgroundColor: theme.palette.agentsList.main,
    cursor: 'pointer',
  },
}));

const ListItemButtonContainer = styled(ListItemButton)(({ theme, selected }) => ({
  borderRadius: '10px',
  '&.Mui-selected': {
    backgroundColor: theme.palette.agentsList.main,
  },
}));

const ListItemIconContainer = styled(ListItemIcon)(({ theme }) => ({
  color: theme.palette.primary.contrastText,
}));

const ListItemTextContainer = styled(ListItemText)(({ theme }) => ({
  fontWeight: 'bold',
}));

function AgentsList({ selectedAgent, setSelectedAgent }: any) {
  const agents = useAgents();

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedAgent(event.target.value);
  };

  function agentComponent(agent: Agent) {
    return (
      <ListItemContainer key={agent.id}>
        <ListItemButtonContainer selected={selectedAgent === agent.id} onClick={() => setSelectedAgent(agent.id)}>
          <ListItemIconContainer>
            {selectedAgent === agent.id ? <AnimatedSmartToyIcon /> : <SmartToyIcon />}
          </ListItemIconContainer>
          <ListItemTextContainer primary={agent.name} />
        </ListItemButtonContainer>
      </ListItemContainer>
    );
  }

  function body() {
    console.debug('AgentsList', agents);
    return (
      <ListContainer>
        {agents.map((agent: Agent) => agentComponent(agent))}
      </ListContainer>
    );
  }

  return <AgentsListContainer>{body()}</AgentsListContainer>;
}

export default AgentsList;


function useAgents() {

  const [agents, setAgents] = useState<Agent[]>([]);

  useEffect(() => {
    async function fetchAgents() {
      // Axios response
      const response = await listAgents();
      console.debug({ response });
      setAgents(response.data);
    }

    fetchAgents();
  }, []);


  return agents;

}
