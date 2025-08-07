import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle } from '@mui/icons-material';
import { Box, Typography } from '@mui/material';
import { toast } from 'react-hot-toast';

export const showSuccessNotification = (message, duration = 3000) => {
  toast.custom((t) => (
    <AnimatePresence>
      {t.visible && (
        <motion.div
          initial={{ opacity: 0, y: -50, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -50, scale: 0.8 }}
          transition={{ duration: 0.3 }}
          style={{
            background: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
            color: 'white',
            padding: '16px 24px',
            borderRadius: '12px',
            boxShadow: '0 8px 32px rgba(76, 175, 80, 0.3)',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            maxWidth: '400px',
            margin: '16px',
          }}
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          >
            <CheckCircle sx={{ fontSize: 24 }} />
          </motion.div>
          <Typography variant="body1" sx={{ fontWeight: 500 }}>
            {message}
          </Typography>
        </motion.div>
      )}
    </AnimatePresence>
  ), { duration });
};

export const showErrorNotification = (message, duration = 4000) => {
  toast.custom((t) => (
    <AnimatePresence>
      {t.visible && (
        <motion.div
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 100 }}
          transition={{ duration: 0.3 }}
          style={{
            background: 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)',
            color: 'white',
            padding: '16px 24px',
            borderRadius: '12px',
            boxShadow: '0 8px 32px rgba(244, 67, 54, 0.3)',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            maxWidth: '400px',
            margin: '16px',
          }}
        >
          <Typography variant="body1" sx={{ fontWeight: 500 }}>
            {message}
          </Typography>
        </motion.div>
      )}
    </AnimatePresence>
  ), { duration });
};
