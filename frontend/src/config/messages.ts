/**
 * Configuração de mensagens e textos do sistema
 * Centraliza todas as strings e mensagens para facilitar manutenção e internacionalização
 */

export const messages = {
  // Mensagens gerais
  common: {
    loading: 'Carregando...',
    error: 'Ocorreu um erro. Tente novamente.',
    success: 'Operação realizada com sucesso!',
    confirm: 'Confirmar',
    cancel: 'Cancelar',
    save: 'Salvar',
    delete: 'Excluir',
    edit: 'Editar',
    back: 'Voltar',
    next: 'Próximo',
    finish: 'Finalizar',
    search: 'Buscar',
    filter: 'Filtrar',
    noResults: 'Nenhum resultado encontrado',
    required: 'Campo obrigatório',
    invalid: 'Valor inválido',
    networkError: 'Erro de conexão. Verifique sua internet.',
    serverError: 'Erro no servidor. Tente novamente mais tarde.',
    unauthorized: 'Sessão expirada. Faça login novamente.',
    forbidden: 'Você não tem permissão para realizar esta ação.',
    notFound: 'Recurso não encontrado.',
    validationError: 'Por favor, corrija os erros antes de continuar.',
  },

  // Mensagens de autenticação
  auth: {
    login: {
      title: 'Bem-vindo de volta!',
      subtitle: 'Faça login para continuar sua jornada espiritual',
      email: 'E-mail',
      password: 'Senha',
      forgotPassword: 'Esqueceu sua senha?',
      noAccount: 'Não tem uma conta?',
      register: 'Cadastre-se',
      error: 'E-mail ou senha inválidos',
    },
    register: {
      title: 'Crie sua conta',
      subtitle: 'Comece sua jornada espiritual hoje',
      name: 'Nome completo',
      email: 'E-mail',
      password: 'Senha',
      confirmPassword: 'Confirmar senha',
      haveAccount: 'Já tem uma conta?',
      login: 'Faça login',
      error: 'Erro ao criar conta. Tente novamente.',
    },
    resetPassword: {
      title: 'Recuperar senha',
      subtitle: 'Digite seu e-mail para receber as instruções',
      email: 'E-mail',
      send: 'Enviar instruções',
      back: 'Voltar ao login',
      success: 'Instruções enviadas para seu e-mail',
      error: 'E-mail não encontrado',
    },
    profile: {
      title: 'Meu perfil',
      subtitle: 'Gerencie suas informações pessoais',
      name: 'Nome',
      email: 'E-mail',
      currentPassword: 'Senha atual',
      newPassword: 'Nova senha',
      confirmPassword: 'Confirmar nova senha',
      save: 'Salvar alterações',
      success: 'Perfil atualizado com sucesso',
      error: 'Erro ao atualizar perfil',
    },
  },

  // Mensagens de estudo
  study: {
    onboarding: {
      title: 'Bem-vindo ao FaleComJesus',
      subtitle: 'Vamos personalizar sua jornada espiritual',
      objectives: {
        title: 'Quais são seus objetivos?',
        subtitle: 'Selecione os temas que mais te interessam',
        options: [
          'Ansiedade e paz interior',
          'Sabedoria e discernimento',
          'Fé e confiança',
          'Amor e relacionamentos',
          'Crescimento espiritual',
          'Serviço e missão',
        ],
      },
      experience: {
        title: 'Qual seu nível de experiência com a Bíblia?',
        subtitle: 'Isso nos ajudará a adaptar o conteúdo',
        options: [
          { value: 'beginner', label: 'Iniciante' },
          { value: 'intermediate', label: 'Intermediário' },
          { value: 'advanced', label: 'Avançado' },
        ],
      },
      preferences: {
        title: 'Como você prefere estudar?',
        subtitle: 'Escolha o formato que melhor se adapta a você',
        options: [
          'Textos curtos e objetivos',
          'Áudios explicativos',
          'Vídeos com reflexões',
          'Exercícios práticos',
        ],
      },
      time: {
        title: 'Qual o melhor horário para seus estudos?',
        subtitle: 'Assim podemos te notificar no momento ideal',
        options: [
          { value: 'morning', label: 'Manhã (6h - 12h)' },
          { value: 'afternoon', label: 'Tarde (12h - 18h)' },
          { value: 'evening', label: 'Noite (18h - 24h)' },
        ],
      },
      success: {
        title: 'Tudo pronto!',
        subtitle: 'Sua jornada espiritual personalizada foi criada',
        start: 'Começar jornada',
      },
    },
    daily: {
      title: 'Estudo do dia',
      subtitle: 'Continue sua jornada espiritual',
      verse: 'Versículo do dia',
      reflection: 'Reflexão',
      notes: 'Suas anotações',
      save: 'Salvar reflexão',
      complete: 'Marcar como concluído',
      next: 'Próximo estudo',
      previous: 'Estudo anterior',
      share: 'Compartilhar',
      audio: 'Ouvir versículo',
      success: 'Reflexão salva com sucesso',
      error: 'Erro ao salvar reflexão',
    },
    plans: {
      title: 'Planos de estudo',
      subtitle: 'Escolha um plano para começar',
      create: 'Criar novo plano',
      edit: 'Editar plano',
      delete: 'Excluir plano',
      progress: 'Progresso',
      duration: 'Duração',
      difficulty: 'Dificuldade',
      start: 'Iniciar plano',
      continue: 'Continuar plano',
      complete: 'Concluir plano',
      certificate: 'Gerar certificado',
      success: 'Plano criado com sucesso',
      error: 'Erro ao criar plano',
    },
  },

  // Mensagens do chat
  chat: {
    title: 'Chat com Jesus',
    subtitle: 'Faça suas perguntas e receba orientação espiritual',
    input: {
      placeholder: 'Digite sua mensagem...',
      send: 'Enviar',
      typing: 'Digitando...',
    },
    limits: {
      free: {
        title: 'Limite de mensagens atingido',
        message: 'Você atingiu o limite de mensagens do plano gratuito',
        watchAd: 'Assistir anúncio para ganhar mais mensagens',
        upgrade: 'Fazer upgrade para plano premium',
      },
      premium: {
        unlimited: 'Mensagens ilimitadas',
      },
    },
    history: {
      title: 'Histórico de conversas',
      empty: 'Nenhuma conversa anterior',
      loadMore: 'Carregar mais',
    },
    error: {
      send: 'Erro ao enviar mensagem',
      load: 'Erro ao carregar histórico',
    },
  },

  // Mensagens de gamificação
  gamification: {
    points: {
      title: 'Seus pontos',
      subtitle: 'Continue sua jornada para ganhar mais pontos',
      total: 'Total de pontos',
      history: 'Histórico de pontos',
      earn: 'Ganhar pontos',
      spend: 'Usar pontos',
    },
    achievements: {
      title: 'Conquistas',
      subtitle: 'Desbloqueie novas conquistas',
      locked: 'Conquista bloqueada',
      unlocked: 'Conquista desbloqueada',
      progress: 'Progresso',
      share: 'Compartilhar conquista',
    },
    rewards: {
      title: 'Recompensas',
      subtitle: 'Troque seus pontos por recompensas',
      available: 'Recompensas disponíveis',
      claimed: 'Recompensas resgatadas',
      claim: 'Resgatar recompensa',
      success: 'Recompensa resgatada com sucesso',
      error: 'Erro ao resgatar recompensa',
    },
  },

  // Mensagens de monetização
  monetization: {
    plans: {
      title: 'Planos disponíveis',
      subtitle: 'Escolha o plano ideal para você',
      free: {
        name: 'Gratuito',
        features: [
          'Acesso básico aos estudos',
          '5 mensagens por dia no chat',
          'Anúncios',
        ],
      },
      premium: {
        name: 'Premium',
        features: [
          'Acesso completo aos estudos',
          'Chat ilimitado',
          'Sem anúncios',
          'Conteúdo exclusivo',
        ],
        price: 'R$ 29,90/mês',
      },
    },
    payment: {
      title: 'Pagamento',
      subtitle: 'Escolha a forma de pagamento',
      methods: {
        credit: 'Cartão de crédito',
        debit: 'Cartão de débito',
        pix: 'PIX',
      },
      card: {
        number: 'Número do cartão',
        name: 'Nome no cartão',
        expiry: 'Validade',
        cvv: 'CVV',
      },
      success: 'Pagamento realizado com sucesso',
      error: 'Erro ao processar pagamento',
    },
    ads: {
      title: 'Assistir anúncio',
      subtitle: 'Ganhe recompensas assistindo anúncios',
      watch: 'Assistir',
      skip: 'Pular',
      complete: 'Anúncio assistido com sucesso',
      error: 'Erro ao processar anúncio',
    },
  },

  // Mensagens de acessibilidade
  accessibility: {
    title: 'Configurações de acessibilidade',
    subtitle: 'Personalize sua experiência',
    fontSize: {
      title: 'Tamanho da fonte',
      small: 'Pequeno',
      medium: 'Médio',
      large: 'Grande',
    },
    contrast: {
      title: 'Contraste',
      normal: 'Normal',
      high: 'Alto',
    },
    screenReader: {
      title: 'Leitor de tela',
      enabled: 'Ativado',
      disabled: 'Desativado',
    },
    audio: {
      title: 'Áudio',
      play: 'Reproduzir',
      pause: 'Pausar',
      stop: 'Parar',
    },
  },

  // Mensagens de erro
  errors: {
    network: {
      title: 'Erro de conexão',
      message: 'Verifique sua conexão com a internet e tente novamente',
      retry: 'Tentar novamente',
    },
    server: {
      title: 'Erro no servidor',
      message: 'Estamos com problemas técnicos. Tente novamente mais tarde',
      contact: 'Contatar suporte',
    },
    validation: {
      title: 'Erro de validação',
      message: 'Por favor, corrija os erros antes de continuar',
      fields: 'Campos com erro',
    },
    auth: {
      title: 'Erro de autenticação',
      message: 'Sua sessão expirou. Faça login novamente',
      login: 'Fazer login',
    },
    payment: {
      title: 'Erro no pagamento',
      message: 'Não foi possível processar seu pagamento',
      retry: 'Tentar novamente',
    },
  },

  // Mensagens de sucesso
  success: {
    profile: {
      title: 'Perfil atualizado',
      message: 'Suas informações foram atualizadas com sucesso',
    },
    study: {
      title: 'Estudo concluído',
      message: 'Parabéns! Você completou mais um estudo',
    },
    reflection: {
      title: 'Reflexão salva',
      message: 'Sua reflexão foi salva com sucesso',
    },
    payment: {
      title: 'Pagamento realizado',
      message: 'Seu pagamento foi processado com sucesso',
    },
    achievement: {
      title: 'Conquista desbloqueada',
      message: 'Parabéns! Você desbloqueou uma nova conquista',
    },
  },

  // Mensagens de confirmação
  confirm: {
    delete: {
      title: 'Confirmar exclusão',
      message: 'Tem certeza que deseja excluir este item?',
      yes: 'Sim, excluir',
      no: 'Não, cancelar',
    },
    logout: {
      title: 'Confirmar saída',
      message: 'Tem certeza que deseja sair?',
      yes: 'Sim, sair',
      no: 'Não, permanecer',
    },
    cancel: {
      title: 'Confirmar cancelamento',
      message: 'Tem certeza que deseja cancelar? Todas as alterações serão perdidas',
      yes: 'Sim, cancelar',
      no: 'Não, continuar',
    },
  },
};

export default messages; 
