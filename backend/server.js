const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage for projects
let projects = [
  { project_id: 'project-alpha', name: 'Project Alpha', created_at: new Date().toISOString() },
  { project_id: 'project-beta', name: 'Project Beta', created_at: new Date().toISOString() },
  { project_id: 'project-gamma', name: 'Project Gamma', created_at: new Date().toISOString() }
];

// GET /api/projects - Get all projects
app.get('/api/projects', (req, res) => {
  console.log('GET /api/projects - Returning all projects');
  res.json(projects);
});

// POST /api/projects - Create a new project
app.post('/api/projects', (req, res) => {
  const { project_id } = req.body;
  
  if (!project_id) {
    return res.status(400).json({ error: 'project_id is required' });
  }

  // Check if project already exists
  const existingProject = projects.find(p => p.project_id === project_id);
  if (existingProject) {
    return res.status(409).json({ error: 'Project already exists' });
  }

  const newProject = {
    project_id,
    name: project_id,
    created_at: new Date().toISOString()
  };

  projects.push(newProject);
  console.log('POST /api/projects - Created new project:', newProject);
  res.status(201).json(newProject);
});

// DELETE /api/projects - Delete a project
app.delete('/api/projects', (req, res) => {
  const { project_id } = req.query;
  
  if (!project_id) {
    return res.status(400).json({ error: 'project_id is required' });
  }

  const projectIndex = projects.findIndex(p => p.project_id === project_id);
  if (projectIndex === -1) {
    return res.status(404).json({ error: 'Project not found' });
  }

  const deletedProject = projects.splice(projectIndex, 1)[0];
  console.log('DELETE /api/projects - Deleted project:', deletedProject);
  res.json({ message: 'Project deleted successfully', project: deletedProject });
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

app.listen(PORT, () => {
  console.log(`🚀 Backend server running on port ${PORT}`);
  console.log(`📊 Available endpoints:`);
  console.log(`   GET  http://localhost:${PORT}/api/projects`);
  console.log(`   POST http://localhost:${PORT}/api/projects`);
  console.log(`   DELETE http://localhost:${PORT}/api/projects`);
  console.log(`   GET  http://localhost:${PORT}/api/health`);
});
