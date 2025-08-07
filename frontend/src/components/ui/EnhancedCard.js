import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, Box } from '@mui/material';
import { animations } from '../../styles/animations';

const EnhancedCard = ({ children, hoverEffect = true, ...props }) => {
  return (
    <motion.div
      {...(hoverEffect ? animations.cardHover : {})}
      transition={animations.transitions.smooth}
    >
      <Card
        {...props}
        sx={{
          ...props.sx,
          borderRadius: 3,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
          transition: 'all 0.3s ease',
          '&:hover': hoverEffect ? {
            boxShadow: '0 12px 40px rgba(0, 0, 0, 0.12)',
            transform: 'translateY(-2px)',
          } : {},
        }}
      >
        <CardContent sx={{ p: 3 }}>
          {children}
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default EnhancedCard;
