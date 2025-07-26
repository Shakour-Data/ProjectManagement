import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProjectManager = ({ onSelectProject }) => {
  const [projects, setProjects] = useState([]);
  const [newProjectId, setNewProjectId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/projects');
      setProjects(response.data);
    } catch (err) {
      setError('Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreateProject = async () => {
    if (!newProjectId.trim()) {
      setError('Project ID cannot be empty');
      return;
    }
    setLoading(true);
    try {
      await axios.post('/api/projects', null, { params: { project_id: newProjectId } });
      setNewProjectId('');
      fetchProjects();
    } catch (err) {
      setError('Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (!window.confirm(`Are you sure you want to delete project "${projectId}"?`)) {
      return;
    }
    setLoading(true);
    try {
      await axios.delete('/api/projects', { params: { project_id: projectId } });
      fetchProjects();
    } catch (err) {
      setError('Failed to delete project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Project Management</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p>Loading...</p>}
      <ul>
        {projects.map((project) => (
          <li key={project}>
            <button onClick={() => onSelectProject(project)}>{project}</button>
            <button onClick={() => handleDeleteProject(project)} style={{ marginLeft: '10px', color: 'red' }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
      <div>
        <input
          type="text"
          placeholder="New project ID"
          value={newProjectId}
          onChange={(e) => setNewProjectId(e.target.value)}
        />
        <button onClick={handleCreateProject} disabled={loading}>
          Create Project
        </button>
      </div>
    </div>
  );
};

export default ProjectManager;
