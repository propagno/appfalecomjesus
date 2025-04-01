/**
 * Configuração dos tipos de validação e regras de negócio
 * Define as regras de validação e regras de negócio do sistema
 */

import * as yup from 'yup';

// Regras de Validação
export const validationRules = {
  // Regras de Autenticação
  auth: {
    // Nome
    name: {
      min: 3,
      max: 100,
      pattern: /^[a-zA-ZÀ-ÿ\s]*$/,
    },
    // Email
    email: {
      pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    },
    // Senha
    password: {
      min: 8,
      max: 50,
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
    },
    // Tentativas de Login
    loginAttempts: {
      max: 5,
      lockoutDuration: 30 * 60 * 1000, // 30 minutos
    },
  },

  // Regras de Estudo
  study: {
    // Plano de Estudo
    plan: {
      title: {
        min: 5,
        max: 100,
      },
      description: {
        min: 10,
        max: 500,
      },
      duration: {
        min: 1,
        max: 365, // dias
      },
    },
    // Sessão
    session: {
      duration: {
        min: 5, // minutos
        max: 120, // minutos
      },
      perDay: {
        max: 5, // sessões
      },
    },
    // Reflexão
    reflection: {
      content: {
        min: 10,
        max: 1000,
      },
      tags: {
        max: 5,
      },
    },
  },

  // Regras de Chat
  chat: {
    // Mensagem
    message: {
      min: 1,
      max: 500,
    },
    // Histórico
    history: {
      max: 100, // mensagens
    },
    // Limites
    limits: {
      free: {
        daily: 5, // mensagens
      },
      premium: {
        daily: 100, // mensagens
      },
    },
  },

  // Regras de Bíblia
  bible: {
    // Busca
    search: {
      min: 3,
      max: 100,
    },
    // Favoritos
    bookmarks: {
      max: 100,
    },
  },

  // Regras de Gamificação
  gamification: {
    // Pontos
    points: {
      study: {
        perSession: 10,
        daily: 50,
      },
      reflection: {
        perReflection: 5,
        daily: 20,
      },
      streak: {
        bonus: 5,
        max: 30,
      },
    },
    // Conquistas
    achievements: {
      max: 50,
    },
  },

  // Regras de Monetização
  monetization: {
    // Anúncios
    ads: {
      daily: {
        max: 3,
      },
      reward: {
        messages: 5,
        points: 10,
      },
    },
    // Assinatura
    subscription: {
      trial: {
        days: 7,
      },
      plans: {
        monthly: {
          price: 19.90,
          features: ['unlimited_chat', 'no_ads', 'premium_content'],
        },
        yearly: {
          price: 199.90,
          features: ['unlimited_chat', 'no_ads', 'premium_content', '2_months_free'],
        },
      },
    },
  },
} as const;

// Schemas de Validação
export const validationSchemas = {
  // Schema de Registro
  register: yup.object().shape({
    name: yup
      .string()
      .min(validationRules.auth.name.min)
      .max(validationRules.auth.name.max)
      .matches(validationRules.auth.name.pattern)
      .required(),
    email: yup
      .string()
      .email()
      .matches(validationRules.auth.email.pattern)
      .required(),
    password: yup
      .string()
      .min(validationRules.auth.password.min)
      .max(validationRules.auth.password.max)
      .matches(validationRules.auth.password.pattern)
      .required(),
    confirmPassword: yup
      .string()
      .oneOf([yup.ref('password')], 'As senhas devem ser iguais')
      .required(),
  }),

  // Schema de Login
  login: yup.object().shape({
    email: yup
      .string()
      .email()
      .matches(validationRules.auth.email.pattern)
      .required(),
    password: yup
      .string()
      .min(validationRules.auth.password.min)
      .max(validationRules.auth.password.max)
      .required(),
  }),

  // Schema de Plano de Estudo
  studyPlan: yup.object().shape({
    title: yup
      .string()
      .min(validationRules.study.plan.title.min)
      .max(validationRules.study.plan.title.max)
      .required(),
    description: yup
      .string()
      .min(validationRules.study.plan.description.min)
      .max(validationRules.study.plan.description.max)
      .required(),
    duration: yup
      .number()
      .min(validationRules.study.plan.duration.min)
      .max(validationRules.study.plan.duration.max)
      .required(),
  }),

  // Schema de Reflexão
  reflection: yup.object().shape({
    content: yup
      .string()
      .min(validationRules.study.reflection.content.min)
      .max(validationRules.study.reflection.content.max)
      .required(),
    tags: yup
      .array()
      .of(yup.string())
      .max(validationRules.study.reflection.tags.max),
  }),

  // Schema de Mensagem do Chat
  chatMessage: yup.object().shape({
    content: yup
      .string()
      .min(validationRules.chat.message.min)
      .max(validationRules.chat.message.max)
      .required(),
  }),
} as const;

export default {
  validationRules,
  validationSchemas,
}; 
