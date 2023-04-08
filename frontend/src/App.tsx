import React from 'react';
import { MainWindow } from './main_window/MainWindow';
import { AppProviders } from './providers/AppProviders';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';

library.add(fas);

function App() {


  return (
    <AppProviders>
      <MainWindow />
    </AppProviders>
  );
}

export default App;
