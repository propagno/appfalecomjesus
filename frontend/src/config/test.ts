/**
 * Configuração de testes
 * Define as configurações para testes unitários, de integração e E2E
 */

export const test = {
  // Configuração do Jest
  jest: {
    // Diretório raiz
    rootDir: '<rootDir>/src',

    // Padrões de arquivos
    testMatch: [
      '**/__tests__/**/*.[jt]s?(x)',
      '**/?(*.)+(spec|test).[jt]s?(x)',
    ],

    // Arquivos a serem ignorados
    testPathIgnorePatterns: [
      '/node_modules/',
      '/dist/',
      '/coverage/',
      '/.next/',
    ],

    // Configuração de cobertura
    coverage: {
      enabled: true,
      threshold: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80,
        },
      },
      reporters: ['text', 'lcov', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        'coverage/',
        '.next/',
        '**/*.d.ts',
        '**/*.test.ts',
        '**/*.spec.ts',
        '**/__tests__/**',
        '**/__mocks__/**',
      ],
    },

    // Configuração de transformação
    transform: {
      '^.+\\.(ts|tsx)$': 'ts-jest',
      '^.+\\.(js|jsx)$': 'babel-jest',
    },

    // Configuração de módulos
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/$1',
      '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
      '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
        '<rootDir>/__mocks__/fileMock.js',
    },

    // Configuração de ambiente
    setupFiles: ['<rootDir>/jest.setup.ts'],
    setupFilesAfterEnv: ['<rootDir>/jest.setup.afterEnv.ts'],

    // Configuração de timeout
    testTimeout: 10000,
  },

  // Configuração do React Testing Library
  rtl: {
    // Configuração de renderização
    render: {
      wrapper: '<rootDir>/test-utils.tsx',
    },

    // Configuração de queries
    queries: {
      // Ordem de prioridade das queries
      order: [
        'getByRole',
        'getByLabelText',
        'getByPlaceholderText',
        'getByText',
        'getByDisplayValue',
        'getByAltText',
        'getByTitle',
        'getByTestId',
      ],

      // Configuração de timeout
      timeout: 1000,
    },

    // Configuração de eventos
    events: {
      // Configuração de delay
      delay: 0,

      // Configuração de debounce
      debounce: 0,
    },
  },

  // Configuração do Cypress
  cypress: {
    // Diretório de testes
    testFiles: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',

    // Configuração de viewport
    viewport: {
      width: 1280,
      height: 720,
    },

    // Configuração de vídeo
    video: {
      enabled: true,
      quality: 'medium',
    },

    // Configuração de screenshots
    screenshots: {
      enabled: true,
      quality: 80,
    },

    // Configuração de retry
    retry: {
      attempts: 2,
      delay: 1000,
    },

    // Configuração de timeout
    timeout: 10000,
  },

  // Configuração de testes E2E
  e2e: {
    // Configuração de ambiente
    environment: {
      development: {
        baseUrl: 'http://localhost:3000',
        apiUrl: 'http://localhost:5000',
      },
      staging: {
        baseUrl: 'https://staging.falecomjesus.com',
        apiUrl: 'https://api-staging.falecomjesus.com',
      },
      production: {
        baseUrl: 'https://falecomjesus.com',
        apiUrl: 'https://api.falecomjesus.com',
      },
    },

    // Configuração de usuários de teste
    users: {
      admin: {
        email: 'admin@falecomjesus.com',
        password: 'admin123',
      },
      user: {
        email: 'user@falecomjesus.com',
        password: 'user123',
      },
      premium: {
        email: 'premium@falecomjesus.com',
        password: 'premium123',
      },
    },

    // Configuração de dados de teste
    data: {
      // Dados da Bíblia
      bible: {
        books: ['Gênesis', 'Êxodo', 'Levítico'],
        chapters: [1, 2, 3],
        verses: [1, 2, 3, 4, 5],
      },

      // Dados de estudo
      study: {
        plans: ['Plano Básico', 'Plano Intermediário', 'Plano Avançado'],
        sections: ['Introdução', 'Desenvolvimento', 'Conclusão'],
        reflections: ['Reflexão 1', 'Reflexão 2', 'Reflexão 3'],
      },

      // Dados de chat
      chat: {
        messages: ['Olá', 'Como posso ajudar?', 'Obrigado'],
      },
    },
  },
} as const;

export default test; 
