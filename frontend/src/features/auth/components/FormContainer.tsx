import React, { ReactNode } from 'react';
import { Link } from 'react-router-dom';

// Logotipo simplificado de FaleComJesus
const Logo = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-spirit-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2L2 7l10 5 10-5-10-5z" />
    <path d="M2 17l10 5 10-5" />
    <path d="M2 12l10 5 10-5" />
  </svg>
);

interface FormContainerProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  verse?: {
    text: string;
    reference: string;
  };
  backLink?: {
    to: string;
    label: string;
  };
}

/**
 * Container para formulários de autenticação com tema espiritual
 */
const FormContainer: React.FC<FormContainerProps> = ({
  children,
  title = "FaleComJesus",
  subtitle,
  verse,
  backLink
}) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-spirit-blue-50 to-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 relative">
        {/* Topo com logo e título */}
        <div className="text-center">
          <div className="flex justify-center">
            <Link to="/" className="inline-flex items-center">
              <Logo />
              <span className="ml-2 text-2xl font-bold text-spirit-blue-700 font-heading">
                {title}
              </span>
            </Link>
          </div>
          
          {subtitle && (
            <h2 className="mt-4 text-xl font-semibold text-spirit-earth-800 font-heading">
              {subtitle}
            </h2>
          )}
          
          {/* Versículo */}
          {verse && (
            <div className="mt-6 p-4 bg-spirit-gold-50 rounded-lg border border-spirit-gold-200 text-center">
              <p className="text-spirit-earth-700 italic font-body">
                "{verse.text}"
              </p>
              <p className="mt-1 text-spirit-earth-600 text-sm font-semibold font-heading">
                {verse.reference}
              </p>
            </div>
          )}
        </div>
        
        {/* Formulário */}
        <div className="mt-8">
          {children}
        </div>
        
        {/* Link de voltar */}
        {backLink && (
          <div className="mt-6 text-center">
            <Link 
              to={backLink.to}
              className="text-spirit-blue-600 hover:text-spirit-blue-800 font-medium transition-colors font-body"
            >
              {backLink.label}
            </Link>
          </div>
        )}
        
        {/* Decoração */}
        <div className="absolute -left-16 -top-10 w-24 h-24 bg-spirit-gold-200 rounded-full opacity-20 blur-xl"></div>
        <div className="absolute -right-10 bottom-10 w-20 h-20 bg-spirit-blue-300 rounded-full opacity-20 blur-xl"></div>
      </div>
    </div>
  );
};

export default FormContainer; 