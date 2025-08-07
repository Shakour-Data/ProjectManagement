import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  Avatar,
  CircularProgress,
  Alert,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Folder as FolderIcon,
  Timeline as TimelineIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { format } from 'date-fns';

const ProjectManager = ({ onSelectProject, onError }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const queryClient = useQueryClient();

  const [openDialog, setOpenDialog] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [editingProject, setEditingProject] = useState(null);

  // Fetch projects using React Query
  const { data: projects = [], isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await axios.get('/api/projects');
      return response.data;
    },
    onError: (error) => {
      onError(error.message);
    },
  });

  // Create project mutation
  const createProjectMutation = useMutation({
    mutationFn: async (projectName) => {
      const response = await axios.post('/api/projects', { project_id: projectName });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['projects']);
      setOpenDialog(false);
      setNewProjectName('');
    },
    onError: (error) => {
      onError(error.message);
    },
  });

  // Delete project mutation
  const deleteProjectMutation = useMutation({
    mutationFn: async (projectId) => {
      await axios.delete('/api/projects', { params: { project_id: projectId } });
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['projects']);
    },
    onError: (error) => {
      onError(error.message);
    },
  });

  const handleCreateProject = () => {
    if (newProjectName.trim()) {
      createProjectMutation.mutate(newProjectName);
    }
  };

  const handleDeleteProject = (projectId) => {
    if (window.confirm(`Are you sure you want to delete project "${projectId}"?`)) {
      deleteProjectMutation.mutate(projectId);
    }
  };

  const handleSelectProject = (projectId) => {
    onSelectProject(projectId);
  };

  return (
    <Box sx={{ p: 3 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4" component="h1" gutterBottom>
            Project Management
          </Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => setOpenDialog(true)}
            sx={{ borderRadius: 2 }}
          >
            Create Project
          </Button>
        </Box>

        {/* Create Project Dialog */}
        <Dialog
          open={openDialog}
          onClose={() => setOpenDialog(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>Create New Project</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Project Name"
              fullWidth
              variant="outlined"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              sx={{ mt: 2 }}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button
              onClick={handleCreateProject}
              color="primary"
              disabled={!newProjectName.trim()}
            >
              Create
            </Button>
          </DialogActions>
        </Dialog>

        {/* Loading State */}
        {isLoading && (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
            <CircularProgress />
          </Box>
        )}

        {/* Error State */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {typeof error === 'string' ? error : error.message || 'An error occurred'}
            </Alert>
          )}

        {/* Projects Grid */}
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid item xs={12} sm={6} md={4} key={project}>
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
              >
                <Card
                  elevation={3}
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    borderRadius: 3,
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 6,
                    },
                  }}
                >
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box display="flex" alignItems="center" mb={2}>
                      <Avatar
                        sx={{
                          bgcolor: 'primary.main',
                          mr: 2,
                        }}
                      >
                        <FolderIcon />
                      </Avatar>
                      <Typography variant="h6" component="h2" noWrap>
                        {project}
                      </Typography>
                    </Box>
                    <Chip
                      label="Active"
                      color="success"
                      size="small"
                      sx={{ mb: 1 }}
                    />
                  </CardContent>
                  <Box p={2} pt={0}>
                    <Box display="flex" justifyContent="space-between">
                      <Button
                        variant="contained"
                        color="primary"
                        size="small"
                        onClick={() => handleSelectProject(project)}
                        startIcon={<FolderIcon />}
                      >
                        Select
                      </Button>
                      <IconButton
                        color="error"
                        onClick={() => handleDeleteProject(project)}
                        size="small"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </motion.div>
    </Box>
  );
};

export default ProjectManager;
