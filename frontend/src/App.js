import React, { Suspense, lazy, useContext, useState } from 'react';
import { ThemeProvider, CssBaseline, Box, IconButton, Typography } from '@mui/material';
import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { lightTheme, darkTheme } from './styles/theme';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { AppContext, AppProvider } from './context/AppContext';

// Lazy load components
const SetupWizard = lazy(() => import('./components/SetupWizard'));
const JsonFileUploader = lazy(() => import('./components/JsonFileUploader'));
const ProjectManager = lazy(() => import('./components/ProjectManager'));
const GanttChart = lazy(() => import('./components/GanttChart'));

// Create a client
const queryClient = new QueryClient();

function AppContent() {
  const {
    step,
    selectedProject,
    handleProjectSelect,
    handleSetupComplete,
    handleUploadComplete,
    handleReset,
  } = useContext(AppContext);

  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const renderContent = () => {
    switch (step) {
      case 'projectManager':
        return <ProjectManager onSelectProject={handleProjectSelect} />;
      case 'setup':
        return <SetupWizard onComplete={handleSetupComplete} projectId={selectedProject} onCancel={handleReset} />;
      case 'upload':
        return <JsonFileUploader onComplete={handleUploadComplete} projectId={selectedProject} onCancel={handleReset} />;
      default:
        return (
          <Box sx={{ p: 3 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Welcome to Project Management Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Select a project to get started or create a new one.
            </Typography>
          </Box>
        );
    }
  };

  return (
    <ThemeProvider theme={darkMode ? darkTheme : lightTheme}>
      <CssBaseline />
      <Box sx={{ position: 'fixed', top: 16, right: 16, zIndex: 1000 }}>
        <IconButton onClick={toggleDarkMode} color="inherit">
          {darkMode ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
      </Box>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            borderRadius: '10px',
            background: darkMode ? '#1e293b' : '#ffffff',
            color: darkMode ? '#f1f5f9' : '#111827',
          },
        }}
      />
      <Suspense fallback={<div>Loading...</div>}>
        {renderContent()}
      </Suspense>
    </ThemeProvider>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </QueryClientProvider>
  );
}

export default App;
