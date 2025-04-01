// Componentes básicos que são importados por outros componentes
import React, { ReactNode } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

// Exportar Card e CardContent
export { Card, CardContent };

// Componente Avatar
export const Avatar: React.FC<{ src?: string; alt?: string; className?: string }> = ({
  src,
  alt = 'Avatar',
  className = '',
}) => (
  <div className={`w-10 h-10 rounded-full overflow-hidden bg-gray-200 ${className}`}>
    {src ? <img src={src} alt={alt} className="w-full h-full object-cover" /> : <div className="w-full h-full flex items-center justify-center text-gray-700">{alt.charAt(0)}</div>}
  </div>
);

// Componente AvatarImage
export const AvatarImage: React.FC<{ src: string; alt?: string }> = ({ src, alt = '' }) => (
  <img src={src} alt={alt} className="h-full w-full object-cover" />
);

// Componente AvatarFallback
export const AvatarFallback: React.FC<{ children: ReactNode }> = ({ children }) => (
  <div className="flex h-full w-full items-center justify-center bg-muted text-muted-foreground">
    {children}
  </div>
);

// Componente Badge
export const Badge: React.FC<{ children: ReactNode; variant?: 'default' | 'secondary' | 'destructive' | 'outline'; className?: string }> = ({ 
  children, 
  variant = 'default',
  className = '' 
}) => {
  const baseStyle = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors';
  
  const variantStyles = {
    default: 'bg-blue-100 text-blue-800',
    secondary: 'bg-gray-100 text-gray-800',
    destructive: 'bg-red-100 text-red-800',
    outline: 'border border-gray-200 text-gray-800',
  };
  
  return (
    <div className={`${baseStyle} ${variantStyles[variant]} ${className}`}>
      {children}
    </div>
  );
};

export const TabsContent: React.FC<{value: string, index: number, children: React.ReactNode}> = 
  ({value, index, children}) => (
    <div role="tabpanel" hidden={value !== index.toString()}>
      {value === index.toString() && children}
    </div>
  );

export const AlertDialog = ({children}: {children: React.ReactNode}) => (
  <div className="alert-dialog">{children}</div>
);

export const AlertDescription: React.FC<{children: React.ReactNode}> = ({children}) => (
  <div className="alert-description">{children}</div>
);

// Exportações padrão
export default {
  Card,
  CardContent,
  Avatar,
  AvatarImage,
  AvatarFallback,
  Badge,
  TabsContent,
  AlertDialog,
  AlertDescription
}; 