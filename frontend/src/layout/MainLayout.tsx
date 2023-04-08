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
      position: 'relative',
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



const MainLayout = (props: any) => {
  const classes = useStyles();



  return (
    <Stack direction={'row'} className={classes.root}>
      {/* Left Part */}
      <Grid item xs={12} md={3} className={classes.sidebar}>
        <AgentsList {...props} />
      </Grid>

      <Grid item xs={12} md={6} >
        <Grid className={classes.mainContent}>
          <ChatWindow {...props} />
        </Grid>
        <Grid item  className={classes.actions}>
          <Actions onSendMessage={props.onSendMessage} {...props} />
        </Grid>
      </Grid>
      {/* Main Content */}


      {/* Right Part */}
      <Grid item xs={12} md={3} className={classes.agentState}>
        <AgentState {...props} />
      </Grid>

      {/* Bottom Chat Window */}

    </Stack>
  );
};

export default MainLayout;
