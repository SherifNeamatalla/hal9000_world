import React from 'react';
import MainLayout from '../layout/MainLayout';
import { makeStyles } from '@material-ui/core/styles';
import { useMainWindowRunner } from './hooks/MainWindowRunner';


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

export function MainWindow() {
  const classes = useStyles();

  const appProps = useMainWindowRunner();


  function sendMessage(message: string): void {
    console.debug('sendMessage', message);
  }

  function body() {
    return (<div className={classes['full-screen-div']}>
      <MainLayout {...(appProps || {})}
                  sendMessage={sendMessage}
      />
    </div>);
  }

  return (<>
    {body()}
  </>);
}
