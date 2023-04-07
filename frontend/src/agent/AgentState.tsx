import React from 'react';
import { styled } from '@mui/system';
import { Divider, List, ListItem, ListItemText, TextField } from '@mui/material';

interface AgentStateProps {
  agentState: any;
  setAgentState: any;
}

const AgentStateContainer = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.agentState.background,
  color: theme.palette.customColors.brightBlueGreen,
  padding: theme.spacing(2),
  height: '100%',
}));

const CommandTextField = styled(TextField)(({ theme }) => ({
  '& input': {
    color: theme.palette.text.primary,
  },
  '& .Mui-disabled': {
    color: theme.palette.text.secondary,
  },
  '& .MuiInputLabel-root': {
    color: theme.palette.customColors.brightGreen2,
  },
}));

function AgentState({ agentState, setAgentState }: AgentStateProps) {
  const [isCommandNameEnabled, setIsCommandNameEnabled] = React.useState(false);
  const [isCommandTypeEnabled, setIsCommandTypeEnabled] = React.useState(false);

  const handleCommandNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAgentState({ ...agentState, commandName: event.target.value });
  };


  const handleCommandTypeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAgentState({ ...agentState, commandType: event.target.value });
  };


  function textFieldComponent(label: any, value: any, setter: any, enabled: any, setEnabled: any) {
    return (<CommandTextField
      label={label}
      fullWidth
      disabled={!enabled}
      value={value}
      onChange={handleCommandNameChange}
      variant={'standard'}
      // InputProps={{
      //   endAdornment: <InputAdornment
      //     style={{ cursor: 'pointer' }}
      //     onClick={() => setEnabled(!enabled)}
      //     position='end'><Edit /></InputAdornment>,
      // }}
    />);
  }

  return (
    <AgentStateContainer>
      <List>
        {(agentState?.goals || ['Goal1', 'Goal2', 'Goal3']) && (
          <>
            <ListItem>
              <ListItemText primary='Agent Goals' />
            </ListItem>
            {(agentState.goals || ['Goal1', 'Goal2', 'Goal3']).map((goal: string, index: number) => (
              <ListItem key={index}>
                <ListItemText primary={goal} />
              </ListItem>
            ))}
            <Divider />
          </>
        )}
        <ListItem>
          {textFieldComponent('Command', agentState.commandName, handleCommandNameChange, isCommandNameEnabled, setIsCommandNameEnabled)}
        </ListItem>
        <ListItem>
          {textFieldComponent('Type', agentState.commandType, handleCommandTypeChange, isCommandTypeEnabled, setIsCommandTypeEnabled)}
        </ListItem>
      </List>
    </AgentStateContainer>
  );
}

export default AgentState;
