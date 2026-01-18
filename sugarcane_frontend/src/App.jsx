import { useState, useEffect } from 'react';
import PredictionForm from './components/PredictionForm';
import Results from './components/Results';
import { healthCheck } from './services/api';
import './App.css';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    console.log('📱 App mounted, checking backend...');
    checkBackend();
  }, []);

  const checkBackend = async () => {
    const status = await healthCheck();
    if (status.status === 'healthy') {
      setBackendStatus('connected');
      console.log('✅ Backend connected');
    } else {
      setBackendStatus('disconnected');
      console.error('❌ Backend disconnected');
      setError('Cannot connect to backend. Make sure backend is running on port 5000.');
    }
  };

  const handleSuccess = (result) => {
    console.log('✅ Prediction successful');
    setPrediction(result);
    setError('');
  };

  const handleError = (errorMsg) => {
    console.error('❌ Error:', errorMsg);
    setError(errorMsg);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🌾 Sugarcane Nutrient Prediction</h1>
        <div className="status">
          <span className={`indicator ${backendStatus}`}></span>
          <span>Backend: {backendStatus === 'connected' ? '✅ Connected' : '❌ Disconnected'}</span>
          <button onClick={checkBackend}>Retry</button>
        </div>
      </header>

      <main className="main">
        {error && <div className="error-box">{error}</div>}

        <div className="content">
          <PredictionForm onSuccess={handleSuccess} onError={handleError} />
          <Results data={prediction} />
        </div>
      </main>

      <footer>
        <p>Sugarcane Nutrient Prediction System</p>
      </footer>
    </div>
  );
}

export default App;
