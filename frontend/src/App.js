import React, { useState } from 'react';
import SetupWizard from './components/SetupWizard';
import JsonFileUploader from './components/JsonFileUploader';
import ProjectManager from './components/ProjectManager';

function App() {
  const [step, setStep] = useState('projectManager'); // 'projectManager', 'setup', 'upload', 'dashboard'
  const [selectedProject, setSelectedProject] = useState(null);

  const handleProjectSelect = (projectId) => {
    setSelectedProject(projectId);
    setStep('setup');
  };

  const handleSetupComplete = () => {
    setStep('upload');
  };

  const handleUploadComplete = () => {
    setStep('dashboard');
  };

  if (step === 'projectManager') {
    return <ProjectManager onSelectProject={handleProjectSelect} />;
  }

  if (step === 'setup') {
    return <SetupWizard onComplete={handleSetupComplete} projectId={selectedProject} />;
  }

  if (step === 'upload') {
    return <JsonFileUploader onComplete={handleUploadComplete} projectId={selectedProject} />;
  }

  // Dashboard placeholder - can be expanded with existing dashboard code
  return (
    <div className="container py-4">
      <h1 className="mb-4">Project Management Dashboard</h1>
      <p>Dashboard content goes here.</p>
    </div>
  );
}

export default App;
