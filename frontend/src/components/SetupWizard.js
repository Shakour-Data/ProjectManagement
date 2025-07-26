import React, { useState } from 'react';
import axios from 'axios';

const steps = [
  { id: 1, title: 'Initialize Git Repository', api: '/setup/init_git' },
  { id: 2, title: 'Create .gitignore', api: '/setup/create_gitignore' },
  { id: 3, title: 'Create requirements.txt', api: '/setup/create_requirements' },
  { id: 4, title: 'Create Virtual Environment', api: '/setup/create_virtualenv' },
  { id: 5, title: 'Install Dependencies', api: '/setup/install_dependencies' },
];

function SetupWizard({ onComplete, projectId }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [status, setStatus] = useState('');
  const [error, setError] = useState(null);

  const runStep = async (step) => {
    setStatus(`Running: ${step.title}...`);
    setError(null);
    try {
      const response = await axios.post(step.api, null, { params: { project_id: projectId } });
      setStatus(response.data.message);
      setTimeout(() => {
        if (currentStep + 1 < steps.length) {
          setCurrentStep(currentStep + 1);
        } else {
          onComplete();
        }
      }, 1000);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
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
          <button onClick={() => runStep(steps[currentStep])}>Retry</button>
        </div>
      ) : (
        <p>{status}</p>
      )}
      <p>Step {currentStep + 1} of {steps.length}</p>
    </div>
  );
}

export default SetupWizard;
