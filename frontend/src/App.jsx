import React, { useState, useEffect } from 'react';

export default function App() {
  const [backendStatus, setBackendStatus] = useState('Checking backend...');

  useEffect(() => {
    fetch('http://localhost:8000/docs')
      .then(res => {
        if (res.ok) setBackendStatus('Connected Successfully to FastAPI Backend!');
        else setBackendStatus('Backend responded with an error.');
      })
      .catch(() => setBackendStatus('Could not connect to FastAPI backend. Is Uvicorn running?'));
  }, []);

  return (
    <div style={{ padding: '3rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Project Acetone Dashboard</h1>
      <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>Operational Control Panel</p>
      
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '12px', border: '1px solid #334155' }}>
        <h3 style={{ marginTop: 0 }}>System Status</h3>
        <p style={{ fontSize: '1.1rem', color: '#38bdf8' }}>{backendStatus}</p>
      </div>
    </div>
  );
}