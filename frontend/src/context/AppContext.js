import React, { createContext, useState } from 'react';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [step, setStep] = useState('projectManager'); // 'projectManager', 'setup', 'upload', 'dashboard'
  const [selectedProject, setSelectedProject] = useState(null);
  const [error, setError] = useState(null);

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

  const handleReset = () => {
    setSelectedProject(null);
    setStep('projectManager');
    setError(null);
  };

  return (
    <AppContext.Provider
      value={{
        step,
        selectedProject,
        error,
        setError,
        handleProjectSelect,
        handleSetupComplete,
        handleUploadComplete,
        handleReset,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};
