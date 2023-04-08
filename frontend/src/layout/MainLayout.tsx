import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import AgentsList from '../agent/AgentsList';
import ChatWindow from '../chat/ChatWindow';
import AgentState from '../agent/AgentState';
import Actions from '../chat/Actions';
import { Stack } from '@mui/material';
// @ts-ignore
// @ts-ignore
const useStyles = makeStyles((theme) => {
  // @ts-ignore
  // @ts-ignore
  return ({
    root: {
      height: '100%',
    },
    sidebar: {
      color: theme.palette.primary.contrastText,
      padding: theme.spacing(2),
      height: '85%',

    },
    mainContent: {
      padding: theme.spacing(2),
      height: '85%',
    },
    actions: {
      height: '15%',
    },
    agentState: {
      padding: theme.spacing(2),
      height: '85%',
    },
  });
});


interface Props {
  selectedAgent: string | null;
  setSelectedAgent: any;
  agentState: any;
  setAgentState: any;
  sendMessage: any;
}

const MainLayout: React.FC<Props> = ({ selectedAgent, setSelectedAgent, agentState, setAgentState, sendMessage }) => {
  const classes = useStyles();

  function onActionClick(action: string): void {
    console.debug('onActionClick', action);
  }

  return (
    <Stack direction={'row'} className={classes.root}>
      {/* Left Part */}
      <Grid item xs={12} md={2} className={classes.sidebar}>
        <AgentsList selectedAgent={selectedAgent} setSelectedAgent={setSelectedAgent} />
      </Grid>

      <Grid item xs={12} md={7} >
        <Grid className={classes.mainContent}>
          <ChatWindow agentState={agentState} sendMessage={sendMessage} />
        </Grid>
        <Grid item  className={classes.actions}>
          <Actions onActionClick={onActionClick} />
        </Grid>
      </Grid>
      {/* Main Content */}


      {/* Right Part */}
      <Grid item xs={12} md={3} className={classes.agentState}>
        <AgentState agentState={agentState} setAgentState={setAgentState} />
      </Grid>

      {/* Bottom Chat Window */}

    </Stack>
  );
};

export default MainLayout;
