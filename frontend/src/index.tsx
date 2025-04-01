import React from 'react';
import { createRoot } from 'react-dom/client';
import { AppProviders } from './app/providers';
import App from './app/App';

// Importar estilos CSS - ordem atualizada para garantir prioridade correta
import './styles/tailwind.output.css'; // Arquivo gerado pelo Tailwind
import './styles/global.css';
import './styles/main.css';

// Adicionar handler global para erros não tratados
window.addEventListener('error', (event) => {
  console.error('Erro global capturado:', event.error);
  // Mostrar mensagem na página para o usuário
  const errorElement = document.createElement('div');
  errorElement.style.position = 'fixed';
  errorElement.style.top = '0';
  errorElement.style.left = '0';
  errorElement.style.right = '0';
  errorElement.style.padding = '10px';
  errorElement.style.backgroundColor = '#f44336';
  errorElement.style.color = 'white';
  errorElement.style.textAlign = 'center';
  errorElement.style.zIndex = '9999';
  errorElement.innerHTML = `Erro na renderização: ${event.error?.message || 'Erro desconhecido'}`;
  document.body.appendChild(errorElement);
});

// Inicializar a aplicação React
console.log('Iniciando renderização do React...');
const container = document.getElementById('root');
if (!container) throw new Error('Failed to find the root element');

const root = createRoot(container);
console.log('Root criado, renderizando App com providers...');

try {
  root.render(
    <React.StrictMode>
      <AppProviders>
        <App />
      </AppProviders>
    </React.StrictMode>
  );
  console.log('Renderização inicial concluída!');
} catch (error) {
  console.error('Erro ao renderizar a aplicação:', error);
  // Mostrar erro diretamente no DOM
  container.innerHTML = `
    <div style="padding: 20px; color: red; text-align: center;">
      <h2>Erro na renderização do React</h2>
      <p>${error instanceof Error ? error.message : 'Erro desconhecido'}</p>
      <p>Verifique o console para mais detalhes.</p>
    </div>
  `;
} 