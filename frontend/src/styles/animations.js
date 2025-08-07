export const animations = {
  fadeInUp: {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6, ease: "easeOut" }
  },
  
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    transition: { duration: 0.4 }
  },
  
  scaleIn: {
    initial: { opacity: 0, scale: 0.9 },
    animate: { opacity: 1, scale: 1 },
    transition: { duration: 0.3 }
  },
  
  slideIn: {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 },
    transition: { duration: 0.4 }
  },
  
  staggerContainer: {
    initial: {},
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  },
  
  hoverScale: {
    whileHover: { scale: 1.05 },
    whileTap: { scale: 0.95 }
  },
  
  cardHover: {
    whileHover: { 
      y: -8,
      transition: { duration: 0.2 }
    }
  }
};

export const transitions = {
  smooth: {
    type: "spring",
    stiffness: 300,
    damping: 30
  },
  
  gentle: {
    type: "spring",
    stiffness: 200,
    damping: 25
  },
  
  quick: {
    type: "spring",
    stiffness: 400,
    damping: 40
  }
};
