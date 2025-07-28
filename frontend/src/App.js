import React, { Suspense, lazy, useContext, useEffect, useState } from 'react';
import ErrorBoundary from './components/ErrorBoundary';
import { AppContext, AppProvider } from './context/AppContext';

const SetupWizard = lazy(() => import('./components/SetupWizard'));
const JsonFileUploader = lazy(() => import('./components/JsonFileUploader'));
const ProjectManager = lazy(() => import('./components/ProjectManager'));
const GanttChart = lazy(() => import('./components/GanttChart'));

function AppContent() {
  const {
    step,
    selectedProject,
    error,
    setError,
    handleProjectSelect,
    handleSetupComplete,
    handleUploadComplete,
    handleReset,
  } = useContext(AppContext);

  const [showGantt, setShowGantt] = useState(false);

  useEffect(() => {
    // Clear error on step change
    setError(null);
  }, [step, setError]);

  if (showGantt) {
    return (
      <div>
        <button onClick={() => setShowGantt(false)} style={{ marginBottom: '20px' }}>
          Back to Dashboard
        </button>
        <GanttChart />
      </div>
    );
  }

  if (step === 'projectManager') {
    return <ProjectManager onSelectProject={handleProjectSelect} onError={setError} />;
  }

  if (step === 'setup') {
    return <SetupWizard onComplete={handleSetupComplete} projectId={selectedProject} onCancel={handleReset} onError={setError} />;
  }

  if (step === 'upload') {
    return <JsonFileUploader onComplete={handleUploadComplete} projectId={selectedProject} onCancel={handleReset} onError={setError} />;
  }

  // Dashboard placeholder - can be expanded with existing dashboard code
  return (
    <ErrorBoundary>
      <div className="container py-4">
        <h1 className="mb-4">Project Management Dashboard</h1>
        <button onClick={handleReset} style={{ marginBottom: '20px', marginRight: '10px' }}>
          Back to Project Manager
        </button>
        <button onClick={() => setShowGantt(true)} style={{ marginBottom: '20px' }}>
          View Gantt Chart
        </button>
        {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
        <p>Dashboard content goes here.</p>
      </div>
    </ErrorBoundary>
  );
}

function App() {
  return (
    <AppProvider>
      <Suspense fallback={<div>Loading...</div>}>
        <AppContent />
      </Suspense>
    </AppProvider>
  );
}

export default App;
