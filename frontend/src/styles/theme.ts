import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1a237e', // Azul marinho
      light: '#534bae',
      dark: '#000051',
    },
    secondary: {
      main: '#ffd700', // Dourado
      light: '#ffff52',
      dark: '#c7a600',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
    text: {
      primary: '#333333',
      secondary: '#666666',
    },
  },
  typography: {
    fontFamily: '"Lora", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontFamily: '"Montserrat", sans-serif',
      fontWeight: 700,
      fontSize: '2.5rem',
    },
    h2: {
      fontFamily: '"Montserrat", sans-serif',
      fontWeight: 600,
      fontSize: '2rem',
    },
    h3: {
      fontFamily: '"Montserrat", sans-serif',
      fontWeight: 600,
      fontSize: '1.75rem',
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.43,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
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
  },
}); 
