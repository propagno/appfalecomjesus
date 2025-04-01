import * as yup from 'yup';

// Regras de validação para autenticação
export const authValidations = {
  register: yup.object().shape({
    name: yup
      .string()
      .required('Nome é obrigatório')
      .min(3, 'Nome deve ter no mínimo 3 caracteres')
      .max(100, 'Nome deve ter no máximo 100 caracteres'),
    email: yup
      .string()
      .required('Email é obrigatório')
      .email('Email inválido')
      .max(255, 'Email deve ter no máximo 255 caracteres'),
    password: yup
      .string()
      .required('Senha é obrigatória')
      .min(8, 'Senha deve ter no mínimo 8 caracteres')
      .matches(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
        'Senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial'
      ),
    confirmPassword: yup
      .string()
      .required('Confirmação de senha é obrigatória')
      .oneOf([yup.ref('password')], 'Senhas não conferem'),
  }),

  login: yup.object().shape({
    email: yup
      .string()
      .required('Email é obrigatório')
      .email('Email inválido'),
    password: yup
      .string()
      .required('Senha é obrigatória'),
  }),

  resetPassword: yup.object().shape({
    email: yup
      .string()
      .required('Email é obrigatório')
      .email('Email inválido'),
  }),

  updateProfile: yup.object().shape({
    name: yup
      .string()
      .min(3, 'Nome deve ter no mínimo 3 caracteres')
      .max(100, 'Nome deve ter no máximo 100 caracteres'),
    email: yup
      .string()
      .email('Email inválido')
      .max(255, 'Email deve ter no máximo 255 caracteres'),
    currentPassword: yup.string(),
    newPassword: yup
      .string()
      .min(8, 'Senha deve ter no mínimo 8 caracteres')
      .matches(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
        'Senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial'
      ),
  }),
};

// Regras de validação para estudo
export const studyValidations = {
  reflection: yup.object().shape({
    content: yup
      .string()
      .required('Conteúdo da reflexão é obrigatório')
      .min(10, 'Reflexão deve ter no mínimo 10 caracteres')
      .max(1000, 'Reflexão deve ter no máximo 1000 caracteres'),
    tags: yup
      .array()
      .of(yup.string())
      .max(5, 'Máximo de 5 tags permitido'),
  }),

  preferences: yup.object().shape({
    objectives: yup
      .array()
      .of(yup.string())
      .min(1, 'Selecione pelo menos um objetivo')
      .max(5, 'Máximo de 5 objetivos permitido'),
    bibleExperienceLevel: yup
      .string()
      .required('Nível de experiência bíblica é obrigatório')
      .oneOf(['iniciante', 'intermediario', 'avancado'], 'Nível inválido'),
    contentPreferences: yup
      .array()
      .of(yup.string())
      .min(1, 'Selecione pelo menos uma preferência de conteúdo')
      .max(3, 'Máximo de 3 preferências permitido'),
    preferredTime: yup
      .string()
      .required('Horário preferido é obrigatório')
      .oneOf(['manha', 'tarde', 'noite'], 'Horário inválido'),
  }),
};

// Regras de validação para chat
export const chatValidations = {
  message: yup.object().shape({
    content: yup
      .string()
      .required('Mensagem é obrigatória')
      .min(10, 'Mensagem deve ter no mínimo 10 caracteres')
      .max(500, 'Mensagem deve ter no máximo 500 caracteres'),
  }),
};

// Regras de validação para feedback
export const feedbackValidations = {
  create: yup.object().shape({
    type: yup
      .string()
      .required('Tipo de feedback é obrigatório')
      .oneOf(['bug', 'feature', 'improvement', 'other'], 'Tipo inválido'),
    title: yup
      .string()
      .required('Título é obrigatório')
      .min(5, 'Título deve ter no mínimo 5 caracteres')
      .max(100, 'Título deve ter no máximo 100 caracteres'),
    description: yup
      .string()
      .required('Descrição é obrigatória')
      .min(20, 'Descrição deve ter no mínimo 20 caracteres')
      .max(1000, 'Descrição deve ter no máximo 1000 caracteres'),
    priority: yup
      .string()
      .required('Prioridade é obrigatória')
      .oneOf(['low', 'medium', 'high', 'urgent'], 'Prioridade inválida'),
  }),
};

// Regras de validação para compartilhamento
export const shareValidations = {
  content: yup.object().shape({
    type: yup
      .string()
      .required('Tipo de conteúdo é obrigatório')
      .oneOf(['verse', 'reflection', 'achievement', 'certificate'], 'Tipo inválido'),
    contentId: yup
      .string()
      .required('ID do conteúdo é obrigatório'),
    platform: yup
      .string()
      .required('Plataforma é obrigatória')
      .oneOf(['whatsapp', 'facebook', 'twitter', 'linkedin', 'email'], 'Plataforma inválida'),
  }),
};

// Regras de validação para configurações
export const settingsValidations = {
  accessibility: yup.object().shape({
    fontSize: yup
      .number()
      .min(12, 'Tamanho mínimo da fonte é 12px')
      .max(24, 'Tamanho máximo da fonte é 24px'),
    highContrast: yup
      .boolean(),
    screenReader: yup
      .boolean(),
  }),

  notifications: yup.object().shape({
    enabled: yup
      .boolean(),
    studyReminders: yup
      .boolean(),
    achievements: yup
      .boolean(),
    chatMessages: yup
      .boolean(),
    systemUpdates: yup
      .boolean(),
  }),
};

// Regras de validação para pagamento
export const paymentValidations = {
  subscription: yup.object().shape({
    plan: yup
      .string()
      .required('Plano é obrigatório')
      .oneOf(['free', 'premium'], 'Plano inválido'),
    paymentMethod: yup
      .string(),
    cardNumber: yup
      .string(),
    expiryDate: yup
      .string(),
    cvv: yup
      .string(),
  }),
}; 
