import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

const EnhancedCard = ({ 
  children, 
  title, 
  subtitle, 
  elevation = 1, 
  hoverEffect = true,
  ...props 
}) => {
  return (
    <motion.div
      whileHover={hoverEffect ? { scale: 1.02, y: -2 } : {}}
      transition={{ duration: 0.2 }}
    >
      <Card elevation={elevation} {...props}>
        {(title || subtitle) && (
          <Box p={3} pb={0}>
            {title && (
              <Typography variant="h6" gutterBottom>
                {title}
              </Typography>
            )}
            {subtitle && (
              <Typography variant="body2" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
        )}
        <CardContent>
          {children}
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default EnhancedCard;
