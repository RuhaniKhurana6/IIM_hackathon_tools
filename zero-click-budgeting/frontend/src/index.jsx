import React from 'react';
import { createRoot } from 'react-dom/client';
import BudgetFuelGauge from './components/BudgetFuelGauge.jsx';

function App(){
  return (
    <div style={{ padding: 20 }}>
      <h3>Budget Fuel Gauge</h3>
      <BudgetFuelGauge percent={35} status="green" />
    </div>
  );
}

createRoot(document.getElementById('root') || document.body).render(<App />);