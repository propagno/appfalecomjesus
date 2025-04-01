// Script de fallback para casos onde o React não carrega
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM carregado');
  
  // Verifica se o elemento root está vazio (React não carregou)
  const root = document.getElementById('root');
  if (root && root.childElementCount === 0) {
    console.log('React não carregou, exibindo interface de fallback');
    
    // Cria elementos HTML básicos para login e registro
    const container = document.createElement('div');
    container.className = 'fallback-container';
    container.style.textAlign = 'center';
    container.style.marginTop = '50px';
    
    const title = document.createElement('h1');
    title.textContent = 'FaleComJesus';
    title.style.marginBottom = '30px';
    
    const buttonContainer = document.createElement('div');
    buttonContainer.style.display = 'flex';
    buttonContainer.style.justifyContent = 'center';
    buttonContainer.style.gap = '20px';
    
    const loginButton = document.createElement('a');
    loginButton.href = '/login';
    loginButton.textContent = 'Entrar';
    loginButton.className = 'fallback-button';
    styleButton(loginButton);
    
    const registerButton = document.createElement('a');
    registerButton.href = '/register';
    registerButton.textContent = 'Cadastrar';
    registerButton.className = 'fallback-button';
    styleButton(registerButton);
    
    buttonContainer.appendChild(loginButton);
    buttonContainer.appendChild(registerButton);
    
    container.appendChild(title);
    container.appendChild(buttonContainer);
    
    // Substitui o conteúdo do root
    root.innerHTML = '';
    root.appendChild(container);
  }
});

// Função para estilizar os botões
function styleButton(button) {
  button.style.backgroundColor = '#4285f4';
  button.style.color = 'white';
  button.style.padding = '10px 20px';
  button.style.borderRadius = '4px';
  button.style.textDecoration = 'none';
  button.style.fontWeight = 'bold';
  button.style.display = 'inline-block';
} 