/**
 * Configuração de build
 * Define as configurações para build, bundling e otimização
 */

export const build = {
  // Configuração do Vite
  vite: {
    // Diretório raiz
    root: process.cwd(),

    // Diretório de build
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: true,
      minify: 'terser',
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom', 'react-router-dom'],
            ui: ['@mui/material', '@emotion/react', '@emotion/styled'],
            utils: ['axios', 'date-fns', 'lodash'],
          },
        },
      },
    },

    // Configuração de servidor
    server: {
      port: 3000,
      host: true,
      open: true,
    },

    // Configuração de plugins
    plugins: [
      'react',
      'typescript',
      'eslint',
      'prettier',
      'tailwindcss',
      'autoprefixer',
    ],
  },

  // Configuração do Babel
  babel: {
    // Presets
    presets: [
      ['@babel/preset-env', { targets: 'defaults' }],
      '@babel/preset-typescript',
      ['@babel/preset-react', { runtime: 'automatic' }],
    ],

    // Plugins
    plugins: [
      '@babel/plugin-transform-runtime',
      '@babel/plugin-proposal-class-properties',
      '@babel/plugin-proposal-object-rest-spread',
    ],

    // Configuração de ambiente
    env: {
      development: {
        plugins: ['react-refresh/babel'],
      },
      production: {
        plugins: [
          ['transform-remove-console', { exclude: ['error', 'warn'] }],
        ],
      },
    },
  },

  // Configuração do TypeScript
  typescript: {
    // Configuração do compilador
    compilerOptions: {
      target: 'ES2020',
      lib: ['DOM', 'DOM.Iterable', 'ESNext'],
      module: 'ESNext',
      skipLibCheck: true,
      moduleResolution: 'bundler',
      allowImportingTsExtensions: true,
      resolveJsonModule: true,
      isolatedModules: true,
      noEmit: true,
      jsx: 'react-jsx',
      strict: true,
      noUnusedLocals: true,
      noUnusedParameters: true,
      noFallthroughCasesInSwitch: true,
      baseUrl: '.',
      paths: {
        '@/*': ['src/*'],
      },
    },

    // Arquivos a serem incluídos
    include: ['src/**/*.ts', 'src/**/*.tsx'],

    // Arquivos a serem excluídos
    exclude: ['node_modules', 'dist', 'build'],
  },

  // Configuração do ESLint
  eslint: {
    // Configuração do parser
    parser: '@typescript-eslint/parser',

    // Configuração de plugins
    plugins: [
      'react',
      'react-hooks',
      '@typescript-eslint',
      'prettier',
      'import',
      'jsx-a11y',
    ],

    // Regras
    rules: {
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      '@typescript-eslint/explicit-module-boundary-types': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'import/order': [
        'error',
        {
          groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
          'newlines-between': 'always',
          alphabetize: { order: 'asc' },
        },
      ],
    },

    // Configuração de ambiente
    env: {
      browser: true,
      es2021: true,
      node: true,
    },
  },

  // Configuração do Prettier
  prettier: {
    // Configuração de formatação
    semi: true,
    singleQuote: true,
    tabWidth: 2,
    printWidth: 100,
    trailingComma: 'es5',
    bracketSpacing: true,
    arrowParens: 'avoid',
    endOfLine: 'auto',

    // Arquivos a serem formatados
    files: ['**/*.{js,jsx,ts,tsx,json,css,scss,md}'],

    // Arquivos a serem ignorados
    ignore: ['node_modules', 'dist', 'build', '.next'],
  },

  // Configuração do Tailwind CSS
  tailwind: {
    // Configuração de conteúdo
    content: ['./src/**/*.{js,jsx,ts,tsx}'],

    // Configuração de tema
    theme: {
      extend: {
        colors: {
          primary: {
            main: '#1E3A8A',
            light: '#3B82F6',
            dark: '#1E40AF',
          },
          secondary: {
            main: '#D4AF37',
            light: '#FCD34D',
            dark: '#B8860B',
          },
        },
        fontFamily: {
          sans: ['Montserrat', 'sans-serif'],
          serif: ['Lora', 'serif'],
        },
      },
    },

    // Plugins
    plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
      require('@tailwindcss/aspect-ratio'),
    ],
  },

  // Configuração de otimização
  optimization: {
    // Configuração de compressão
    compression: {
      enabled: true,
      algorithm: 'gzip',
      threshold: 10240, // 10KB
    },

    // Configuração de cache
    cache: {
      enabled: true,
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 dias
    },

    // Configuração de imagens
    images: {
      quality: 80,
      format: ['webp', 'avif'],
    },
  },
} as const;

export default build; 
