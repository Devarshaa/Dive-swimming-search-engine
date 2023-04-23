import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Helmet } from 'react-helmet';
global.process = require('process');
global.Buffer = require('buffer').Buffer;

const root = ReactDOM.createRoot(document.getElementById('root'));

const csp = `
  default-src 'self';
  frame-src 'self' https://www.google.com;
  script-src 'self' https://www.google.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data:;
  font-src 'self';
  connect-src 'self';
`;

root.render(
    <React.StrictMode>
      <Helmet>
        <meta http-equiv="Content-Security-Policy" content={csp} />
      </Helmet>
      <App />
    </React.StrictMode>
  );

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
