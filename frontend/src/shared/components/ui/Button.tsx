import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  leftIcon,
  rightIcon,
  fullWidth = false,
  className = '',
  children,
  ...props
}) => {
  // Classes base
  const baseClasses = 'flex items-center justify-center font-medium rounded-md transition-all focus:outline-none';
  
  // Classes de tamanho
  const sizeClasses = {
    sm: 'text-xs py-1.5 px-3',
    md: 'text-sm py-2.5 px-5',
    lg: 'text-base py-3 px-6',
  };
  
  // Classes de variante com tema bíblico
  const variantClasses = {
    // Azul marinho profundo - cor principal, transmite confiança e espiritualidade
    primary: 'bg-[#1a365d] text-white hover:bg-[#2a4a7c] focus:ring-2 focus:ring-[#1a365d]/50',
    
    // Dourado angelical - cor secundária para ênfase e destaque
    secondary: 'bg-[#c9a55c] text-[#1a365d] hover:bg-[#d4b978] focus:ring-2 focus:ring-[#c9a55c]/50',
    
    // Bordas sutis com fundo claro
    outline: 'border border-[#c9a55c] bg-white text-[#1a365d] hover:bg-[#f7f2e5] focus:ring-2 focus:ring-[#c9a55c]/30',
    
    // Sem fundo, apenas texto
    ghost: 'bg-transparent text-[#1a365d] hover:bg-[#f7f2e5] focus:ring-2 focus:ring-[#f7f2e5]',
    
    // Estilo de link, com sublinhado
    link: 'bg-transparent text-[#3d6491] hover:text-[#1a365d] hover:underline p-0 focus:ring-0',
    
    // Vermelho suave para alertas e ações destrutivas
    danger: 'bg-[#933a16] text-white hover:bg-[#b24a24] focus:ring-2 focus:ring-[#933a16]/50',
    
    // Verde para mensagens positivas e ações de sucesso
    success: 'bg-[#3c6e71] text-white hover:bg-[#2c5456] focus:ring-2 focus:ring-[#3c6e71]/50',
  };
  
  // Classes para estado desabilitado
  const disabledClasses = 'opacity-60 cursor-not-allowed';
  
  // Classes de largura total
  const widthClasses = fullWidth ? 'w-full' : '';
  
  return (
    <button
      className={`
        ${baseClasses}
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        ${(disabled || loading) ? disabledClasses : ''}
        ${widthClasses}
        shadow-sm
        ${className}
      `}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className="mr-2">
          <svg className="animate-spin h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
      )}
      
      {!loading && leftIcon && <span className="mr-2">{leftIcon}</span>}
      <span className="truncate">{children}</span>
      {!loading && rightIcon && <span className="ml-2">{rightIcon}</span>}
    </button>
  );
};

export default Button; 