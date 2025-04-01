/**
 * Configuração de CI/CD
 * Define as configurações para integração contínua e deploy contínuo
 */

export const ci = {
  // Configuração do GitHub Actions
  githubActions: {
    // Workflows
    workflows: {
      // Workflow de CI
      ci: {
        name: 'CI',
        on: {
          push: {
            branches: ['main', 'develop'],
          },
          pull_request: {
            branches: ['main', 'develop'],
          },
        },
        jobs: {
          // Job de lint
          lint: {
            name: 'Lint',
            runsOn: 'ubuntu-latest',
            steps: [
              {
                name: 'Checkout',
                uses: 'actions/checkout@v3',
              },
              {
                name: 'Setup Node.js',
                uses: 'actions/setup-node@v3',
                with: {
                  'node-version': '18',
                },
              },
              {
                name: 'Install dependencies',
                run: 'npm ci',
              },
              {
                name: 'Run ESLint',
                run: 'npm run lint',
              },
              {
                name: 'Run Prettier',
                run: 'npm run format:check',
              },
            ],
          },

          // Job de testes
          test: {
            name: 'Test',
            runsOn: 'ubuntu-latest',
            steps: [
              {
                name: 'Checkout',
                uses: 'actions/checkout@v3',
              },
              {
                name: 'Setup Node.js',
                uses: 'actions/setup-node@v3',
                with: {
                  'node-version': '18',
                },
              },
              {
                name: 'Install dependencies',
                run: 'npm ci',
              },
              {
                name: 'Run tests',
                run: 'npm test',
              },
              {
                name: 'Upload coverage',
                uses: 'codecov/codecov-action@v3',
                with: {
                  file: './coverage/lcov.info',
                  fail_ci_if_error: true,
                },
              },
            ],
          },

          // Job de build
          build: {
            name: 'Build',
            runsOn: 'ubuntu-latest',
            steps: [
              {
                name: 'Checkout',
                uses: 'actions/checkout@v3',
              },
              {
                name: 'Setup Node.js',
                uses: 'actions/setup-node@v3',
                with: {
                  'node-version': '18',
                },
              },
              {
                name: 'Install dependencies',
                run: 'npm ci',
              },
              {
                name: 'Build',
                run: 'npm run build',
              },
              {
                name: 'Upload build',
                uses: 'actions/upload-artifact@v3',
                with: {
                  name: 'build',
                  path: 'dist',
                },
              },
            ],
          },
        },
      },

      // Workflow de CD
      cd: {
        name: 'CD',
        on: {
          push: {
            branches: ['main'],
          },
        },
        jobs: {
          // Job de deploy
          deploy: {
            name: 'Deploy',
            runsOn: 'ubuntu-latest',
            needs: ['lint', 'test', 'build'],
            steps: [
              {
                name: 'Checkout',
                uses: 'actions/checkout@v3',
              },
              {
                name: 'Setup Node.js',
                uses: 'actions/setup-node@v3',
                with: {
                  'node-version': '18',
                },
              },
              {
                name: 'Install dependencies',
                run: 'npm ci',
              },
              {
                name: 'Download build',
                uses: 'actions/download-artifact@v3',
                with: {
                  name: 'build',
                  path: 'dist',
                },
              },
              {
                name: 'Deploy to production',
                run: 'npm run deploy',
                env: {
                  NODE_ENV: 'production',
                  AWS_ACCESS_KEY_ID: '${{ secrets.AWS_ACCESS_KEY_ID }}',
                  AWS_SECRET_ACCESS_KEY: '${{ secrets.AWS_SECRET_ACCESS_KEY }}',
                  AWS_REGION: '${{ secrets.AWS_REGION }}',
                },
              },
            ],
          },
        },
      },
    },
  },

  // Configuração do Docker
  docker: {
    // Configuração de build
    build: {
      // Contexto
      context: '.',

      // Dockerfile
      dockerfile: 'Dockerfile',

      // Tags
      tags: ['falecomjesus:latest', 'falecomjesus:${{ github.sha }}'],

      // Argumentos
      args: {
        NODE_ENV: 'production',
        VITE_API_URL: '${{ secrets.VITE_API_URL }}',
      },
    },

    // Configuração de push
    push: {
      // Registro
      registry: 'ghcr.io',

      // Organização
      organization: 'falecomjesus',

      // Imagem
      image: 'falecomjesus',

      // Tags
      tags: ['latest', '${{ github.sha }}'],
    },

    // Configuração de deploy
    deploy: {
      // Servidor
      server: {
        host: '${{ secrets.DOCKER_HOST }}',
        port: 2375,
        key: '${{ secrets.DOCKER_KEY }}',
        cert: '${{ secrets.DOCKER_CERT }}',
        ca: '${{ secrets.DOCKER_CA }}',
      },

      // Stack
      stack: {
        name: 'falecomjesus',
        file: 'docker-compose.yml',
      },
    },
  },

  // Configuração de monitoramento
  monitoring: {
    // Configuração de logs
    logs: {
      // Serviço
      service: 'falecomjesus',

      // Nível
      level: 'info',

      // Retenção
      retention: '30d',
    },

    // Configuração de métricas
    metrics: {
      // Serviço
      service: 'falecomjesus',

      // Intervalo
      interval: '1m',

      // Retenção
      retention: '7d',
    },

    // Configuração de alertas
    alerts: {
      // Canal
      channel: 'slack',

      // Nível
      level: 'error',

      // Cooldown
      cooldown: '1h',
    },
  },
} as const;

export default ci; 
