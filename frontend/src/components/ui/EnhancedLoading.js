import React from 'react';
import { motion } from 'framer-motion';
import { Box, Typography, CircularProgress } from '@mui/material';
import { animations } from '../../styles/animations';

const EnhancedLoading = ({ message = "در حال بارگذاری..." }) => {
  return (
    <motion.div
      {...animations.fadeInUp}
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '200px',
        gap: '20px'
      }}
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
      >
        <CircularProgress 
          size={60}
          thickness={4}
          sx={{
            color: 'primary.main',
            '& .MuiCircularProgress-circle': {
              strokeLinecap: 'round',
            }
          }}
        />
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <Typography 
          variant="h6" 
          color="text.secondary"
          sx={{ fontWeight: 300 }}
        >
          {message}
        </Typography>
      </motion.div>
    </motion.div>
  );
};

export default EnhancedLoading;
