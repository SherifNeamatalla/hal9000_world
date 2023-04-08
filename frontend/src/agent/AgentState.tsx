import React from 'react';
import { styled } from '@mui/system';
import { Divider, List, ListItem, ListItemText, TextField, useTheme } from '@mui/material';

interface AgentStateProps {
  command: any;
  goals: any;
}

const AgentStateContainer = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.agentState.background,
  color: theme.palette.customColors.brightGreen2,
  padding: theme.spacing(2),
  height: '100%',
  borderRadius: '10px',
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

function AgentState({ command, goals }: AgentStateProps) {

  const theme = useTheme();


  function commandComponent() {
    if (!command) {
      return null;
    }

    return (<>
      <ListItem>
        <ListItemText style={{
          color: (theme.palette as any).customColors.brightYellow,
          fontWeight: 'bold',
          textAlign: 'center',
        }}>
          Command
        </ListItemText>


      </ListItem>
      <ListItem>

      </ListItem>
      <ListItem>
        <ListItemText style={{
          color: (theme.palette as any).customColors.brightGreen,
          fontWeight: 'bold',
        }}>
          Name: {command?.name}
        </ListItemText>
      </ListItem>

      <ListItem>
        <ListItemText style={{
          color: (theme.palette as any).customColors.brightGreen,
          fontWeight: 'bold',
        }}>
          Type: {command?.type}
        </ListItemText>
      </ListItem>

      <ListItem>
        <ListItemText style={{
          color: (theme.palette as any).customColors.brightGreen,
          fontWeight: 'bold',
        }}>
          Args:
        </ListItemText>

        <List>
          {Object.keys(command?.args || {}).map((argKey: string, index: number) => (
            <ListItem key={argKey}>
              <ListItemText style={{}}>
                {argKey}:{command.args[argKey]}
              </ListItemText>
            </ListItem>
          ))}
        </List>
      </ListItem>
    </>);
  }

  return (
    <AgentStateContainer>
      <List>
        {(goals || []) && (
          <>
            <ListItem>
              <ListItemText
                style={{
                  color: (theme.palette as any).customColors.brightYellow,
                  fontWeight: 'bold',
                }}
                primary='Agent Goals' />
            </ListItem>
            {(goals || []).map((goal: string, index: number) => (
              <ListItem key={index}>
                <ListItemText primary={(index + 1) + '. ' + goal} />
              </ListItem>
            ))}
            <Divider />
          </>
        )}
        {commandComponent()}
      </List>
    </AgentStateContainer>
  );
}

export default AgentState;
