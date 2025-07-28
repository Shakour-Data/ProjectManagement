import React, { useState } from 'react';
import axios from 'axios';

const steps = [
  { id: 1, title: 'Initialize Git Repository', api: '/setup/init_git' },
  { id: 2, title: 'Create .gitignore', api: '/setup/create_gitignore' },
  { id: 3, title: 'Create requirements.txt', api: '/setup/create_requirements' },
  { id: 4, title: 'Create Virtual Environment', api: '/setup/create_virtualenv' },
  { id: 5, title: 'Install Dependencies', api: '/setup/install_dependencies' },
];

function SetupWizard({ onComplete, projectId, onCancel, onError }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [status, setStatus] = useState('');
  const [error, setError] = useState(null);
  const [running, setRunning] = useState(false);

  const runStep = async (step) => {
    setRunning(true);
    setStatus(`Running: ${step.title}...`);
    setError(null);
    onError(null);
    try {
      const response = await axios.post(step.api, null, { params: { project_id: projectId } });
      setStatus(response.data.message);
      setTimeout(() => {
        if (currentStep + 1 < steps.length) {
          setCurrentStep(currentStep + 1);
        } else {
          setRunning(false);
          onComplete();
        }
      }, 1000);
    } catch (err) {
      const errMsg = err.response?.data?.detail || err.message;
      setError(errMsg);
      onError(errMsg);
      setRunning(false);
    }
  };

  React.useEffect(() => {
    if (currentStep < steps.length) {
      runStep(steps[currentStep]);
    }
  }, [currentStep]);

  return (
    <div>
      <h2>Project Setup Wizard</h2>
      {error ? (
        <div style={{ color: 'red' }}>
          <p>Error: {error}</p>
          <button onClick={() => runStep(steps[currentStep])} disabled={running}>Retry</button>
        </div>
      ) : (
        <p>{status}</p>
      )}
      <p>Step {currentStep + 1} of {steps.length}</p>
      <button onClick={onCancel} disabled={running} style={{ marginTop: '10px' }}>Cancel Setup</button>
    </div>
  );
}

export default SetupWizard;
