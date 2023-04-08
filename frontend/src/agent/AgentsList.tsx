import React from 'react';
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
  color: theme.palette.customColors.brightGreen2,
}));

const ListItemTextContainer = styled(ListItemText)(({ theme }) => ({
  fontWeight: 'bold',
  color: theme.palette.customColors.brightGreen2,
}));

function AgentsList({ selectedAgentId, setSelectedAgentId, agents }: any) {


  function agentComponent(agent: Agent) {
    return (
      <ListItemContainer key={agent.id}>
        <ListItemButtonContainer selected={selectedAgentId === agent.id} onClick={() => setSelectedAgentId(agent.id)}>
          <ListItemIconContainer>
            {selectedAgentId === agent.id ? <AnimatedSmartToyIcon /> : <SmartToyIcon />}
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
        {(agents || []).map((agent: Agent) => agentComponent(agent))}
      </ListContainer>
    );
  }

  return <AgentsListContainer>{body()}</AgentsListContainer>;
}

export default AgentsList;

