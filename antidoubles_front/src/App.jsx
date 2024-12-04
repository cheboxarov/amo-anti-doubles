
import React, { useEffect } from 'react'
import DoublesWindow from "./pages/DoublesWindow"
import { useSignals } from '@preact/signals-react/runtime';
import { winState, WIN_STATES } from './signals/pageStateSignals';
import AdminWindow from './pages/AdminWindow';
import { updateMe } from './services/doublesServices';

const App = () => {

  useSignals()

  useEffect(async () => {
    await updateMe()
  }, [])

  if (winState.value == WIN_STATES.DOUBLES) {
    return (
        <div>
            <DoublesWindow />
        </div>
    ) 
  } else if (winState.value == WIN_STATES.ADMIN) {
    return (
        <div>
            <AdminWindow />
        </div>
    )
  }
};

export default App;
