import React, { forwardRef } from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ 
    label, 
    helperText, 
    error, 
    leftIcon, 
    rightIcon, 
    fullWidth = true, 
    className = '', 
    id,
    ...props 
  }, ref) => {
    // ID gerado para o input, caso não seja fornecido
    const inputId = id || `input-${Math.random().toString(36).substring(2, 11)}`;
    
    // Estilos para o container do input
    const containerClasses = `
      ${fullWidth ? 'w-full' : 'w-auto'}
      ${className}
    `;
    
    // Estilos para o label
    const labelClasses = `
      block text-sm font-medium font-heading 
      ${error ? 'text-spirit-red-500' : 'text-spirit-blue-700'}
      mb-1.5
    `;
    
    // Estilos para o wrapper do input (para posicionar ícones)
    const inputWrapperClasses = `
      relative flex items-center
      ${error ? 'focus-within:ring-spirit-red-400' : 'focus-within:ring-spirit-blue-400'}
      focus-within:ring-2 rounded-md
    `;
    
    // Estilos para o input
    const inputClasses = `
      w-full py-2.5 px-3 
      ${leftIcon ? 'pl-10' : ''}
      ${rightIcon ? 'pr-10' : ''}
      bg-white
      border rounded-md shadow-sm
      font-body text-base leading-relaxed
      text-spirit-blue-800 placeholder:text-spirit-blue-300
      transition-colors duration-200
      focus:outline-none
      focus:border-spirit-blue-500
      disabled:bg-spirit-blue-50 disabled:cursor-not-allowed
      ${error 
        ? 'border-spirit-red-400 focus:border-spirit-red-500' 
        : 'border-spirit-earth-200 hover:border-spirit-blue-300'
      }
    `;
    
    // Estilos para texto auxiliar
    const helperTextClasses = `
      mt-1.5 text-xs
      ${error ? 'text-spirit-red-500' : 'text-spirit-blue-500'}
    `;
    
    return (
      <div className={containerClasses}>
        {label && (
          <label htmlFor={inputId} className={labelClasses}>
            {label}
          </label>
        )}
        
        <div className={inputWrapperClasses}>
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-spirit-blue-400">
              {leftIcon}
            </div>
          )}
          
          <input
            id={inputId}
            ref={ref}
            className={inputClasses}
            aria-invalid={!!error}
            aria-describedby={error ? `${inputId}-error` : undefined}
            {...props}
          />
          
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-spirit-blue-400">
              {rightIcon}
            </div>
          )}
        </div>
        
        {(error || helperText) && (
          <p 
            id={error ? `${inputId}-error` : undefined} 
            className={helperTextClasses}
          >
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input; 