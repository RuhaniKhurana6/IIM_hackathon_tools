import React from 'react';

export default function BudgetFuelGauge({ percent = 0, status = 'green' }) {
  const color = status === 'red' ? '#e11d48' : status === 'orange' ? '#f59e0b' : '#10b981';
  return (
    <div style={{ width: 240 }}>
      <div style={{ height: 20, background: '#eee', borderRadius: 10 }}>
        <div style={{ width: `${percent}%`, height: 20, background: color, borderRadius: 10 }} />
      </div>
      <div style={{ marginTop: 8 }}>Budget usage: {percent}% ({status})</div>
    </div>
  );
}