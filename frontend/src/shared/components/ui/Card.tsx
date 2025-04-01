import React from 'react';

export interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
  footer?: React.ReactNode;
  titleIcon?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  children,
  title,
  subtitle,
  className = '',
  footer,
  titleIcon,
}) => {
  return (
    <div className={`
      bg-white rounded-lg overflow-hidden
      shadow-spirit
      border border-spirit-earth-100
      ${className}
    `}>
      {(title || subtitle) && (
        <div className="px-6 pt-6 pb-4">
          {title && (
            <div className="flex items-center mb-1">
              {titleIcon && (
                <span className="mr-3 text-spirit-gold-400">
                  {titleIcon}
                </span>
              )}
              <h2 className="text-xl font-semibold text-spirit-blue-700 font-heading">
                {title}
              </h2>
            </div>
          )}
          
          {subtitle && (
            <p className="text-sm text-spirit-earth-600 font-body">
              {subtitle}
            </p>
          )}
        </div>
      )}
      
      <div className="px-6 py-5">
        {children}
      </div>
      
      {footer && (
        <div className="px-6 py-4 bg-spirit-blue-50 border-t border-spirit-earth-100">
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card; 