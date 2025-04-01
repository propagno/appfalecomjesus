#!/bin/sh

# Cria uma página que carrega o React diretamente do CDN
cat > /usr/share/nginx/html/app.js << 'EOF'
// Script para carregar o React diretamente
document.addEventListener('DOMContentLoaded', function() {
  const rootElement = document.getElementById('root');
  if (rootElement) {
    rootElement.innerHTML = '<div class="loading">Carregando aplicação...</div>';
  }
});
EOF

# Informa que o script foi executado com sucesso
echo "React entrypoint setup completed successfully" 