import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import DoublesWindows from './pages/DoublesWindow';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <DoublesWindows />
  </React.StrictMode>
);


reportWebVitals();
