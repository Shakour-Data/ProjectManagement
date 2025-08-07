import React from 'react';
import { CircularProgress, Box } from '@mui/material';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ size = 40, color = 'primary' }) => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="200px"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <CircularProgress size={size} color={color} />
      </motion.div>
    </Box>
  );
};

export default LoadingSpinner;
