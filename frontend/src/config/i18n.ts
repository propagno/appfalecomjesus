/**
 * Configuração de internacionalização
 * Define as configurações de idiomas, formatação e traduções
 */

export const i18n = {
  // Idiomas suportados
  languages: {
    pt: {
      code: 'pt',
      name: 'Português',
      nativeName: 'Português',
      direction: 'ltr',
    },
    en: {
      code: 'en',
      name: 'English',
      nativeName: 'English',
      direction: 'ltr',
    },
    es: {
      code: 'es',
      name: 'Español',
      nativeName: 'Español',
      direction: 'ltr',
    },
  },

  // Idioma padrão
  defaultLanguage: 'pt',

  // Configuração de formatação
  format: {
    // Formatação de data
    date: {
      short: {
        pt: 'dd/MM/yyyy',
        en: 'MM/dd/yyyy',
        es: 'dd/MM/yyyy',
      },
      medium: {
        pt: 'dd MMM yyyy',
        en: 'MMM dd, yyyy',
        es: 'dd MMM yyyy',
      },
      long: {
        pt: 'dd MMMM yyyy',
        en: 'MMMM dd, yyyy',
        es: 'dd MMMM yyyy',
      },
    },

    // Formatação de hora
    time: {
      short: {
        pt: 'HH:mm',
        en: 'hh:mm a',
        es: 'HH:mm',
      },
      medium: {
        pt: 'HH:mm:ss',
        en: 'hh:mm:ss a',
        es: 'HH:mm:ss',
      },
      long: {
        pt: 'HH:mm:ss.SSS',
        en: 'hh:mm:ss.SSS a',
        es: 'HH:mm:ss.SSS',
      },
    },

    // Formatação de número
    number: {
      decimal: {
        pt: ',',
        en: '.',
        es: ',',
      },
      thousand: {
        pt: '.',
        en: ',',
        es: '.',
      },
      currency: {
        pt: 'BRL',
        en: 'USD',
        es: 'EUR',
      },
    },

    // Formatação de texto
    text: {
      capitalize: true,
      trim: true,
      maxLength: 1000,
    },
  },

  // Configuração de fallback
  fallback: {
    // Idioma de fallback
    language: 'en',

    // Chaves de fallback
    keys: {
      // Chaves que não precisam de tradução
      skipTranslation: [
        'name',
        'email',
        'password',
        'phone',
        'address',
        'city',
        'state',
        'country',
        'zip',
      ],

      // Chaves que devem manter o texto original
      keepOriginal: [
        'bible.books',
        'bible.chapters',
        'bible.verses',
        'study.plans',
        'study.sections',
      ],
    },
  },

  // Configuração de carregamento
  loading: {
    // Estratégia de carregamento
    strategy: 'lazy',

    // Prefixo dos arquivos de tradução
    prefix: 'locales/',

    // Sufixo dos arquivos de tradução
    suffix: '.json',

    // Cache de traduções
    cache: {
      enabled: true,
      maxAge: 24 * 60 * 60 * 1000, // 24 horas
    },
  },

  // Configuração de detecção
  detection: {
    // Ordem de detecção
    order: ['querystring', 'cookie', 'localStorage', 'navigator', 'path', 'subdomain'],

    // Chaves de detecção
    keys: {
      querystring: 'lang',
      cookie: 'i18next',
      localStorage: 'i18nextLng',
      path: 'lang',
      subdomain: 'lang',
    },

    // Cache de detecção
    cache: {
      enabled: true,
      maxAge: 24 * 60 * 60 * 1000, // 24 horas
    },
  },

  // Configuração de debug
  debug: {
    // Habilitar logs
    enabled: process.env.NODE_ENV === 'development',

    // Nível de log
    level: 'info',

    // Prefixo dos logs
    prefix: '[i18n]',
  },
} as const;

export default i18n; 
