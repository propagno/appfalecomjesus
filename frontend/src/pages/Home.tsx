import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthContext } from '../features/auth/contexts/AuthContext';
import '../styles/auth.css';

// Ícones consistentes com o padrão de auth
const BookIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 19.5C4 18.837 4.26339 18.2011 4.73223 17.7322C5.20107 17.2634 5.83696 17 6.5 17H20" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M6.5 2H20V22H6.5C5.83696 22 5.20107 21.7366 4.73223 21.2678C4.26339 20.7989 4 20.163 4 19.5V4.5C4 3.83696 4.26339 3.20107 4.73223 2.73223C5.20107 2.26339 5.83696 2 6.5 2V2Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const BibleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 6V22" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M6 8H18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M3 2V22H21V2H3Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M9 12H15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ChatIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ProgressIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 12H18L15 21L9 3L6 12H2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

/**
 * Página inicial que exibe o resumo da jornada espiritual do usuário
 */
const HomePage: React.FC = () => {
  const { user } = useAuthContext();

  return (
    <div className="auth-container">
      <div className="auth-card" style={{ maxWidth: "800px" }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 className="auth-title">Bem-vindo à sua jornada espiritual, {user?.name}</h1>
          <p style={{ fontStyle: 'italic', color: '#666', marginBottom: '20px' }}>
            "O Senhor é meu pastor e nada me faltará." - Salmos 23:1
          </p>
        </div>

        {/* Progresso */}
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
            <ProgressIcon />
            <h2 style={{ marginLeft: '10px', fontSize: '1.2rem', fontWeight: 'bold' }}>Seu Progresso</h2>
          </div>
          <div style={{ height: '10px', width: '100%', backgroundColor: '#E5E5E5', borderRadius: '10px', overflow: 'hidden' }}>
            <div 
              style={{ 
                height: '100%', 
                width: '42%', 
                background: 'linear-gradient(to right, #CCE4F6, #F4D58D)',
                borderRadius: '10px'
              }} 
            />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '5px', fontSize: '0.9rem', color: '#666' }}>
            <span>Progresso: 42%</span>
            <span>Continue sua jornada</span>
          </div>
        </div>

        {/* Principais opções */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          {/* Card de Plano Atual */}
          <div style={{ border: '1px solid #E5E5E5', borderRadius: '10px', padding: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
              <BookIcon />
              <h3 style={{ marginLeft: '10px', fontSize: '1.1rem', fontWeight: 'bold' }}>Seu Plano de Hoje</h3>
            </div>
            <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1.5rem' }}>
              Continue sua jornada de aprendizado e cresça em sua fé diariamente.
            </p>
            <Link to="/study">
              <button className="auth-button" style={{ margin: 0 }}>
                Continuar Estudando
              </button>
            </Link>
          </div>
          
          {/* Card da Bíblia */}
          <div style={{ border: '1px solid #E5E5E5', borderRadius: '10px', padding: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
              <BibleIcon />
              <h3 style={{ marginLeft: '10px', fontSize: '1.1rem', fontWeight: 'bold' }}>Explorar a Bíblia</h3>
            </div>
            <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1.5rem' }}>
              Aprofunde-se na palavra de Deus, explore capítulos e versículos.
            </p>
            <Link to="/bible">
              <button className="auth-button" style={{ margin: 0 }}>
                Abrir Bíblia
              </button>
            </Link>
          </div>
          
          {/* Card do Chat */}
          <div style={{ border: '1px solid #E5E5E5', borderRadius: '10px', padding: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
              <ChatIcon />
              <h3 style={{ marginLeft: '10px', fontSize: '1.1rem', fontWeight: 'bold' }}>Chat com IA</h3>
            </div>
            <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1.5rem' }}>
              Converse sobre temas espirituais e esclareça suas dúvidas.
            </p>
            <Link to="/chat">
              <button className="auth-button" style={{ margin: 0 }}>
                Iniciar Conversa
              </button>
            </Link>
          </div>
        </div>
        
        {/* Última reflexão */}
        <div style={{ 
          border: '1px solid #E5E5E5', 
          borderRadius: '10px', 
          padding: '1.5rem',
          marginBottom: '1rem',
          background: 'rgba(204, 228, 246, 0.1)'
        }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '10px' }}>Sua Última Reflexão</h3>
          <p style={{ fontStyle: 'italic', fontSize: '0.9rem', color: '#666' }}>
            "Aprendi hoje que confiar em Deus significa entregar completamente meus medos e preocupações. 
            Quando leio Filipenses 4:6-7, sinto uma paz que não consigo explicar com palavras..."
          </p>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            marginTop: '15px',
            fontSize: '0.8rem',
            color: '#888'
          }}>
            <span>23 de Março, 2025</span>
            <Link to="/reflections" style={{ color: '#007BFF', textDecoration: 'none' }}>
              Ver todas as reflexões
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 