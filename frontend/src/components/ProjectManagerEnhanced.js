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
  useTheme,
  useMediaQuery,
  Fade,
  Zoom,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Folder as FolderIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { format } from 'date-fns';
import EnhancedLoading from './ui/EnhancedLoading';
import EnhancedCard from './ui/EnhancedCard';
import { showSuccessNotification, showErrorNotification } from './ui/SuccessNotification';
import { animations } from '../styles/animations';

const ProjectManagerEnhanced = ({ onSelectProject }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const queryClient = useQueryClient();

  const [openDialog, setOpenDialog] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');

  const { data: projects = [], isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await axios.get('/api/projects');
      return response.data;
    },
  });

  const createProjectMutation = useMutation({
    mutationFn: async (projectName) => {
      const response = await axios.post('/api/projects', { project_id: projectName });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['projects']);
      setOpenDialog(false);
      setNewProjectName('');
      showSuccessNotification('پروژه با موفقیت ایجاد شد!');
    },
    onError: (error) => {
      showErrorNotification('خطا در ایجاد پروژه: ' + error.message);
    },
  });

  const deleteProjectMutation = useMutation({
    mutationFn: async (projectId) => {
      await axios.delete('/api/projects', { params: { project_id: projectId } });
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['projects']);
      showSuccessNotification('پروژه با موفقیت حذف شد!');
    },
  });

  const handleCreateProject = () => {
    if (newProjectName.trim()) {
      createProjectMutation.mutate(newProjectName);
    }
  };

  const handleSelectProject = (projectId) => {
    onSelectProject(projectId);
    showSuccessNotification(`پروژه "${projectId}" انتخاب شد`);
  };

  const handleDeleteProject = (projectId) => {
    if (window.confirm(`آیا از حذف پروژه "${projectId}" مطمئن هستید؟`)) {
      deleteProjectMutation.mutate(projectId);
    }
  };

  if (isLoading) {
    return <EnhancedLoading message="در حال بارگذاری پروژه‌ها..." />;
  }

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Box 
          display="flex" 
          justifyContent="space-between" 
          alignItems="center" 
          mb={4}
          sx={{ flexDirection: { xs: 'column', sm: 'row' }, gap: 2 }}
        >
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Typography variant="h4" component="h1" sx={{ fontWeight: 700, color: 'primary.main' }}>
              مدیریت پروژه‌ها
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              پروژه‌های خود را مدیریت کنید و به راحتی ایجاد کنید
            </Typography>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Button
              variant="contained"
              color="primary"
              size="large"
              startIcon={<AddIcon />}
              onClick={() => setOpenDialog(true)}
              sx={{
                borderRadius: 3,
                px: 4,
                py: 1.5,
                fontWeight: 600,
                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
                '&:hover': {
                  boxShadow: '0 8px 30px rgba(0, 0, 0, 0.15)',
                  transform: 'translateY(-2px)',
                },
              }}
            >
              ایجاد پروژه جدید
            </Button>
          </motion.div>
        </Box>

        {/* Create Project Dialog */}
        <Dialog
          open={openDialog}
          onClose={() => setOpenDialog(false)}
          maxWidth="sm"
          fullWidth
          TransitionComponent={Fade}
        >
          <DialogTitle sx={{ fontWeight: 600, textAlign: 'center' }}>
            ایجاد پروژه جدید
          </DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="نام پروژه"
              fullWidth
              variant="outlined"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              sx={{ mt: 2 }}
              placeholder="مثلا: پروژه وب‌سایت"
            />
          </DialogContent>
          <DialogActions sx={{ p: 3 }}>
            <Button onClick={() => setOpenDialog(false)} color="secondary">
              انصراف
            </Button>
            <Button
              onClick={handleCreateProject}
              color="primary"
              variant="contained"
              disabled={!newProjectName.trim()}
              sx={{ borderRadius: 2 }}
            >
              ایجاد
            </Button>
          </DialogActions>
        </Dialog>

        {/* Projects Grid */}
        <AnimatePresence>
          {isLoading ? (
            <EnhancedLoading message="در حال بارگذاری پروژه‌ها..." />
          ) : error ? (
            <Alert severity="error" sx={{ mb: 3 }}>
              خطا در بارگذاری پروژه‌ها: {error.message}
            </Alert>
          ) : projects.length === 0 ? (
            <EnhancedCard>
              <CardContent sx={{ textAlign: 'center', py: 8 }}>
                <FolderIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  هنوز پروژه‌ای ایجاد نشده
                </Typography>
                <Typography variant="body2" color="text.secondary" mb={3}>
                  برای شروع، یک پروژه جدید ایجاد کنید
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<AddIcon />}
                  onClick={() => setOpenDialog(true)}
                >
                  ایجاد اولین پروژه
                </Button>
              </CardContent>
            </EnhancedCard>
          ) : (
            <Grid container spacing={3}>
              {projects.map((project, index) => (
                <Grid item xs={12} sm={6} md={4} key={project}>
                  <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <EnhancedCard hoverEffect>
                      <CardContent sx={{ position: 'relative' }}>
                        <Box display="flex" alignItems="center" mb={2}>
                          <Avatar
                            sx={{
                              bgcolor: 'primary.main',
                              mr: 2,
                              width: 48,
                              height: 48,
                            }}
                          >
                            <FolderIcon />
                          </Avatar>
                          <Box>
                            <Typography variant="h6" noWrap sx={{ fontWeight: 600 }}>
                              {project}
                            </Typography>
                            <Chip
                              label="فعال"
                              color="success"
                              size="small"
                              sx={{ mt: 0.5 }}
                            />
                          </Box>
                        </Box>

                        <Box display="flex" justifyContent="space-between" alignItems="center" mt={3}>
                          <Button
                            variant="contained"
                            color="primary"
                            size="small"
                            onClick={() => handleSelectProject(project)}
                            sx={{ borderRadius: 2 }}
                          >
                            انتخاب
                          </Button>
                          <IconButton
                            color="error"
                            onClick={() => handleDeleteProject(project)}
                            size="small"
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Box>
                      </CardContent>
                    </EnhancedCard>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          )}
        </AnimatePresence>
      </motion.div>
    </Box>
  );
};

export default ProjectManagerEnhanced;
