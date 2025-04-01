import { createTheme, Theme } from '@mui/material/styles';
import { styled } from '@mui/material/styles';
import { motion } from 'framer-motion';

// Paleta de Cores
export const colors = {
  primary: {
    main: '#0A2463',
    light: '#3E92CC',
    dark: '#061539',
    contrastText: '#FFFFFF',
  },
  secondary: {
    main: '#3E92CC',
    light: '#64A8D8',
    dark: '#2B668F',
    contrastText: '#FFFFFF',
  },
  accent: {
    main: '#FFD700',
    light: '#FFE44D',
    dark: '#B29700',
    contrastText: '#000000',
  },
  error: {
    main: '#FF0000',
    light: '#FF3333',
    dark: '#B20000',
    contrastText: '#FFFFFF',
  },
  warning: {
    main: '#FFA500',
    light: '#FFB733',
    dark: '#B27300',
    contrastText: '#000000',
  },
  info: {
    main: '#00BFFF',
    light: '#33CCFF',
    dark: '#0085B2',
    contrastText: '#000000',
  },
  success: {
    main: '#00FF00',
    light: '#33FF33',
    dark: '#00B200',
    contrastText: '#000000',
  },
  text: {
    primary: '#333333',
    secondary: '#666666',
    disabled: '#999999',
  },
  background: {
    default: '#FFFFFF',
    paper: '#F5F5F5',
  },
};

// Tipografia
export const typography = {
  fontFamily: [
    'Montserrat',
    'Lora',
    'sans-serif',
  ].join(','),
  h1: {
    fontFamily: 'Lora, serif',
    fontWeight: 700,
    fontSize: '2.5rem',
  },
  h2: {
    fontFamily: 'Lora, serif',
    fontWeight: 700,
    fontSize: '2rem',
  },
  h3: {
    fontFamily: 'Lora, serif',
    fontWeight: 600,
    fontSize: '1.75rem',
  },
  h4: {
    fontFamily: 'Lora, serif',
    fontWeight: 600,
    fontSize: '1.5rem',
  },
  h5: {
    fontFamily: 'Lora, serif',
    fontWeight: 500,
    fontSize: '1.25rem',
  },
  h6: {
    fontFamily: 'Lora, serif',
    fontWeight: 500,
    fontSize: '1rem',
  },
  body1: {
    fontFamily: 'Lora, serif',
    fontSize: '1rem',
    lineHeight: 1.6,
  },
  body2: {
    fontFamily: 'Lora, serif',
    fontSize: '0.875rem',
    lineHeight: 1.6,
  },
  button: {
    fontFamily: 'Montserrat, sans-serif',
    fontWeight: 600,
    textTransform: 'none' as const,
  },
};

// Componentes Base
export const components = {
  MuiButton: {
    styleOverrides: {
      root: {
        borderRadius: 30,
        boxShadow: 'none',
        fontWeight: 600,
        padding: '10px 16px',
        transition: 'all 0.3s ease',
        '&:hover': {
          boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
          transform: 'translateY(-2px)',
        },
      },
      contained: {
        boxShadow: 'none',
        '&:hover': {
          boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
        },
      },
    },
  },
  MuiCard: {
    styleOverrides: {
      root: {
        borderRadius: 12,
        overflow: 'hidden',
        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 8px 12px rgba(0, 0, 0, 0.15)',
        },
      },
    },
  },
  MuiTextField: {
    styleOverrides: {
      root: {
        '& .MuiOutlinedInput-root': {
          borderRadius: 8,
        },
      },
    },
  },
  MuiPaper: {
    styleOverrides: {
      root: {
        borderRadius: 12,
      },
    },
  },
};

// Tema Base
export const baseTheme = createTheme({
  palette: colors,
  typography,
  components,
  shape: {
    borderRadius: 8,
  },
  spacing: 8,
});

// Componentes Estilizados
export const StyledContainer = styled('div')(({ theme }) => ({
  padding: theme.spacing(4),
  maxWidth: '1200px',
  margin: '0 auto',
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
  },
}));

export const PageContainer = styled(motion.div)(({ theme }) => ({
  minHeight: '100vh',
  backgroundColor: theme.palette.background.default,
}));

export const CardContainer = styled(motion.div)(({ theme }) => ({
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
  gap: theme.spacing(3),
  padding: theme.spacing(3),
}));

export const LoadingOverlay = styled('div')(({ theme }) => ({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(255, 255, 255, 0.8)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: theme.zIndex.modal + 1,
}));

export const ActionFeedback = styled(motion.div)(({ theme }) => ({
  position: 'fixed',
  bottom: theme.spacing(2),
  right: theme.spacing(2),
  padding: theme.spacing(2),
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.success.main,
  color: theme.palette.success.contrastText,
  boxShadow: theme.shadows[3],
}));

// Animações
export const pageTransition = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: { duration: 0.3 }
};

export const cardHoverAnimation = {
  hover: {
    scale: 1.02,
    transition: { duration: 0.2 }
  }
};

// Utilitários
export const flexCenter = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

export const textGradient = {
  background: 'linear-gradient(45deg, #0A2463 30%, #3E92CC 90%)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
}; 
