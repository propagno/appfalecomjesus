import React, { forwardRef } from 'react';

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  error?: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, error, className = '', id, ...props }, ref) => {
    // ID gerado para o checkbox, caso não seja fornecido
    const checkboxId = id || `checkbox-${Math.random().toString(36).substring(2, 11)}`;
    
    return (
      <div className={`flex items-start ${className}`}>
        <div className="flex items-center h-5">
          <input
            ref={ref}
            id={checkboxId}
            type="checkbox"
            className="w-4 h-4 text-spirit-blue-600 border-spirit-earth-300 rounded
                       focus:ring-spirit-blue-500 focus:ring-2
                       checked:bg-spirit-blue-600
                       hover:border-spirit-blue-400
                       cursor-pointer"
            aria-invalid={!!error}
            aria-describedby={error ? `${checkboxId}-error` : undefined}
            {...props}
          />
        </div>
        
        <div className="ml-2 text-sm">
          {label && (
            <label 
              htmlFor={checkboxId} 
              className="font-body text-spirit-earth-700 cursor-pointer"
            >
              {label}
            </label>
          )}
          
          {error && (
            <p 
              id={`${checkboxId}-error`} 
              className="mt-1 text-xs text-spirit-red-500"
            >
              {error}
            </p>
          )}
        </div>
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';

export default Checkbox; 