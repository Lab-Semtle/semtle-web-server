
// react 17.0.2
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { CookiesProvider } from 'react-cookie';
import axios from 'axios';

axios.defaults.withCredentials = true;

ReactDOM.render(
  <React.StrictMode>
    <CookiesProvider>
      <App/>
    </CookiesProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

