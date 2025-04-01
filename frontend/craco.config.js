const path = require('path');

module.exports = {
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@base': path.resolve(__dirname, 'src/components/base'),
      '@contexts': path.resolve(__dirname, 'src/contexts'),
      '@constants': path.resolve(__dirname, 'src/constants'),
      '@hooks': path.resolve(__dirname, 'src/hooks'),
      '@layouts': path.resolve(__dirname, 'src/layouts'),
      '@pages': path.resolve(__dirname, 'src/pages'),
      '@services': path.resolve(__dirname, 'src/services'),
      '@styles': path.resolve(__dirname, 'src/styles'),
      '@types': path.resolve(__dirname, 'src/types'),
      '@utils': path.resolve(__dirname, 'src/utils'),
      '@app': path.resolve(__dirname, 'src/app'),
      '@features': path.resolve(__dirname, 'src/features'),
      '@shared': path.resolve(__dirname, 'src/shared'),
      '@lib': path.resolve(__dirname, 'src/lib'),
      '@auth': path.resolve(__dirname, 'src/features/auth'),
      '@bible': path.resolve(__dirname, 'src/features/bible'),
      '@chat': path.resolve(__dirname, 'src/features/chat'),
      '@study': path.resolve(__dirname, 'src/features/study'),
      '@gamification': path.resolve(__dirname, 'src/features/gamification'),
      '@monetization': path.resolve(__dirname, 'src/features/monetization'),
      '@admin': path.resolve(__dirname, 'src/features/admin'),
    },
    configure: (webpackConfig) => {
      // Adicionar source maps para melhor debugging
      webpackConfig.devtool = 'source-map';
      return webpackConfig;
    }
  },
  style: {
    postcss: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ],
    },
  },
  devServer: {
    port: 3000,
    proxy: {
      '/api': {
        target: process.env.REACT_APP_API_URL || 'http://localhost:80',
        changeOrigin: true,
        secure: false,
        headers: {
          Connection: 'keep-alive'
        },
        // Aumentar o timeout para lidar com respostas lentas do servidor
        timeout: 60000,
        // Não reescreva o caminho para preservar a estrutura /api
        pathRewrite: function(path) {
          // Manter /api em todas as rotas exceto health check
          if (path === '/api/auth/health') {
            return '/api/auth/health';
          }
          return path;
        },
        onProxyReq: (proxyReq) => {
          // Adicionar cabeçalhos para melhorar a detecção de problemas
          proxyReq.setHeader('X-Frontend-Request', 'true');
        },
        onError: (err, req, res) => {
          // Manipular erros de proxy
          console.error('Erro de proxy:', err);
          res.writeHead(502, {
            'Content-Type': 'application/json',
          });
          res.end(JSON.stringify({ 
            status: 'error', 
            message: 'Não foi possível conectar ao servidor backend',
            error: err.message
          }));
        },
      },
    },
    // Adicionar opções para melhor debugging e logs
    client: {
      overlay: {
        errors: true,
        warnings: false,
      },
      logging: 'verbose',
    },
  },
}; 