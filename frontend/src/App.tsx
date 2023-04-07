import React, { useState } from 'react';
import MainLayout from './layout/MainLayout';
import { AppProviders } from './providers/AppProviders';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  'full-screen-div': {
    'width': '100vw',
    'height': '100vh',
    'min-height': '100%',
    'box-sizing': 'border-box',
    'overflow-x': 'hidden',
    'overflow-y': 'hidden',
  },
}));


function App() {
  const classes = useStyles();
  const [agentState, setAgentState] = useState({});

  const [selectedAgent, setSelectedAgent] = useState(null);


  function sendMessage(message: string): void {
    console.debug('sendMessage', message);
  }

  return (
    <AppProviders>
      <div className={classes['full-screen-div']}>
        <MainLayout selectedAgent={selectedAgent}
                    setSelectedAgent={setSelectedAgent}
                    agentState={agentState} setAgentState={setAgentState} sendMessage={sendMessage} />
      </div>
    </AppProviders>
  );
}

export default App;
