import axios, { AxiosError } from 'axios';

/**
 * Interface para resultado da verificação de conexão
 */
interface ConnectionCheckResult {
  success: boolean;
  message: string;
  details?: string;
  statusCode?: number;
}

interface ConnectionResult {
  success: boolean;
  message: string;
  details?: string;
  statusCode?: number;
  errorType?: string;
}

interface RouteTestResult {
  success: boolean;
  statusCode?: number;
  message?: string;
  time?: number;
  detailedError?: any;
}

interface DiagnosticResult {
  summary: string;
  routes: Record<string, RouteTestResult>;
  recommendations: string[];
}

/**
 * Verifica a conexão com o servidor de autenticação
 * Detecta erros de timeout, CORS e outros problemas de rede
 */
export const checkAuthConnection = async (): Promise<ConnectionResult> => {
  try {
    // Testar o endpoint exato que sabemos que funciona
    const response = await axios.get('/api/auth/health', {
      timeout: 7000, // 7 segundos de timeout
      withCredentials: true // Importante para cookies de sessão
    });
    
    return {
      success: true,
      message: `Conexão com o servidor estabelecida com sucesso.`,
      statusCode: response.status,
      details: `Tempo de resposta: ${response.headers['x-response-time'] || 'não disponível'}`
    };
  } catch (error: any) {
    console.error('Erro ao verificar conexão com o servidor:', error);
    
    // Extrair informações do erro para diagnóstico
    const statusCode = error.response?.status;
    const errorMessage = error.message || 'Erro desconhecido';
    const errorCode = error.code;
    
    // Verificar se é um erro de CORS
    if (errorMessage.includes('CORS') || error.response?.headers?.['access-control-allow-origin'] === null) {
      return {
        success: false,
        message: 'Erro de CORS detectado.',
        details: 'Verifique as configurações de CORS no servidor e no proxy do frontend.',
        statusCode
      };
    }
    
    // Erro de timeout
    if (errorCode === 'ECONNABORTED' || statusCode === 504) {
      return {
        success: false,
        message: 'Timeout ao conectar com o servidor.',
        details: 'O servidor não respondeu dentro do tempo limite. Pode estar sobrecarregado ou inacessível no momento.',
        statusCode: 504
      };
    }
    
    // Erro de gateway (502)
    if (statusCode === 502) {
      return {
        success: false,
        message: 'Erro de Gateway.',
        details: `O NGINX não conseguiu se comunicar com o serviço de autenticação. Erro: ${error.response?.data?.error || 'Desconhecido'}`,
        statusCode: 502
      };
    }
    
    // Servidor não encontrado
    if (statusCode === 404) {
      return {
        success: false,
        message: 'Endpoint de health check não encontrado.',
        details: 'Verifique se a rota /api/auth/health existe no backend.',
        statusCode: 404
      };
    }
    
    // Erro de rede
    if (errorMessage === 'Network Error') {
      return {
        success: false,
        message: 'Erro de rede.',
        details: 'Verifique se o servidor está disponível, se o endereço está correto e se as configurações de proxy estão adequadas.',
        statusCode
      };
    }
    
    // Erro genérico com mais detalhes para debugging
    return {
      success: false,
      message: `Falha na conexão: ${errorMessage}`,
      details: `Código: ${errorCode}, Status: ${statusCode || 'N/A'}, Resposta: ${JSON.stringify(error.response?.data || {})}`,
      statusCode
    };
  }
};

// Tenta verificar a conexão com timeout progressivo
export const tryConnectWithRetry = async (maxRetries = 2): Promise<ConnectionResult> => {
  let lastError: any;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      // Aumenta o timeout a cada tentativa
      const timeout = 2000 + attempt * 3000; // 2s, 5s, 8s...
      
      // Tenta conectar com timeout progressivo
      const response = await axios.get('/api/auth/health', {
        timeout,
        withCredentials: true
      });
      
      // Se chegou aqui, conectou com sucesso
      return {
        success: true,
        message: 'Servidor online e funcionando corretamente',
        details: `Resposta: ${response.status} ${response.statusText}`
      };
    } catch (error: any) {
      lastError = error;
      
      // Se for um erro que não é de conexão/timeout, não tenta novamente
      if (error.response && ![502, 504].includes(error.response.status)) {
        break;
      }
      
      // Aguarda antes da próxima tentativa (exceto na última)
      if (attempt < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }
  
  // Após todas as tentativas, retorna o último erro
  return processError(lastError);
};

/**
 * Processa o erro para fornecer detalhes mais específicos
 */
function processError(error: any): ConnectionResult {
  // Erro de CORS
  if (error.message?.includes('CORS')) {
    return {
      success: false,
      message: 'Erro de CORS: O servidor rejeitou a solicitação',
      details: 'O servidor não permite solicitações do frontend. Verifique a configuração de CORS.',
      errorType: 'CORS'
    };
  }
  
  // Timeout
  if (error.code === 'ECONNABORTED') {
    return {
      success: false,
      message: 'Timeout: O servidor demorou muito para responder',
      details: 'O servidor pode estar sobrecarregado ou inacessível. Tente novamente mais tarde.',
      errorType: 'TIMEOUT'
    };
  }
  
  // Erro de gateway (502 Bad Gateway)
  if (error.response && error.response.status === 502) {
    return {
      success: false,
      message: 'Erro de Gateway: Servidor backend não está respondendo',
      details: 'O NGINX não consegue se comunicar com o serviço de autenticação. Verifique se o ms-auth está funcionando.',
      statusCode: 502,
      errorType: 'GATEWAY'
    };
  }
  
  // Erro de timeout do gateway (504 Gateway Timeout)
  if (error.response && error.response.status === 504) {
    return {
      success: false,
      message: 'Gateway Timeout: O servidor backend demorou muito para responder',
      details: 'O NGINX tentou se comunicar com o ms-auth, mas houve timeout. Verifique se o serviço está sobrecarregado.',
      statusCode: 504,
      errorType: 'GATEWAY_TIMEOUT'
    };
  }
  
  // Erro de rede genérico
  if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
    return {
      success: false,
      message: 'Erro de rede: Não foi possível conectar ao servidor',
      details: 'Verifique sua conexão com a internet ou se o servidor está em execução.',
      errorType: 'NETWORK'
    };
  }
  
  // Outros erros
  return {
    success: false,
    message: 'Erro ao conectar com o servidor',
    details: error.message || 'Erro desconhecido',
    statusCode: error.response?.status,
    errorType: 'UNKNOWN'
  };
}

/**
 * Testa uma rota específica com timeout ajustado e registra detalhes da resposta
 */
export const testRoute = async (route: string, timeoutMs = 5000): Promise<RouteTestResult> => {
  const startTime = Date.now();
  try {
    console.log(`Tentando ${route} com timeout ${timeoutMs}ms`);
    
    const response = await axios.get(route, {
      timeout: timeoutMs,
      withCredentials: true,
      headers: {
        'Accept': 'application/json',
        'X-Debug': 'true'
      }
    });
    
    const time = Date.now() - startTime;
    console.log(`Sucesso para ${route}: status=${response.status}, tempo=${time}ms`);
    console.log(`Headers de resposta:`, response.headers);
    
    return {
      success: response.status >= 200 && response.status < 300,
      statusCode: response.status,
      message: `OK (${response.statusText})`,
      time
    };
  } catch (error: any) {
    const time = Date.now() - startTime;
    console.log(`Erro para ${route}: tempo=${time}ms`);
    
    let statusCode: number | undefined;
    let message = error.message;
    let detailedError = {};
    
    if (error.response) {
      statusCode = error.response.status;
      message = `${error.message} (Status: ${statusCode})`;
      
      // Registrar detalhes sobre a resposta de erro
      console.log(`Detalhes do erro HTTP:`, {
        status: error.response.status,
        statusText: error.response.statusText,
        headers: error.response.headers,
        data: error.response.data
      });
      
      detailedError = {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data
      };
    } else if (error.request) {
      // A requisição foi feita mas não houve resposta
      console.log(`Nenhuma resposta recebida:`, error.request);
      message = 'Sem resposta do servidor';
    } else if (error.code === 'ECONNABORTED') {
      console.log(`Timeout:`, error);
      message = 'Timeout - Servidor não respondeu no tempo esperado';
    } else if (error.code === 'ERR_NETWORK') {
      console.log(`Erro de rede:`, error);
      message = 'Erro de rede - Servidor indisponível';
    } else {
      // Algo aconteceu durante a configuração da requisição
      console.log(`Erro de configuração:`, error.message);
    }
    
    return {
      success: false,
      statusCode,
      message,
      time,
      detailedError
    };
  }
};

/**
 * Realiza diagnóstico testando múltiplas rotas possíveis
 */
export const diagnosticAuth = async (): Promise<DiagnosticResult> => {
  const routes = {
    'api/auth/health': '/api/auth/health',
    'api/v1/auth/health': '/api/v1/auth/health',
    'root-health': '/health'
  };
  
  // Testes com diferentes configurações
  const testConfigs = [
    { name: 'default', route: '/api/auth/health', config: {} },
    { name: 'no-cors', route: '/api/auth/health', config: { withCredentials: false } },
    { name: 'no-cache', route: '/api/auth/health', config: { 
      headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' } 
    }},
    { name: 'fetch-api', route: '/api/auth/health', useFetch: true },
  ];
  
  const results: Record<string, RouteTestResult> = {};
  const recommendations: string[] = [];
  
  // Testar todas as rotas
  for (const [key, route] of Object.entries(routes)) {
    console.log(`Testando rota: ${route}`);
    try {
      results[key] = await testRoute(route);
    } catch (err) {
      console.error(`Erro inesperado ao testar ${route}:`, err);
      results[key] = { 
        success: false, 
        message: 'Erro inesperado: ' + (err instanceof Error ? err.message : String(err)),
        time: 0
      };
    }
  }
  
  // Testar com diferentes configurações
  for (const config of testConfigs) {
    try {
      if (config.useFetch) {
        // Usar a API fetch como alternativa ao Axios
        const startTime = Date.now();
        const response = await fetch(config.route, {
          method: 'GET',
          credentials: 'include',
          cache: 'no-cache',
          headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'fetch'
          }
        });
        const time = Date.now() - startTime;
        
        const success = response.ok;
        const responseText = await response.text();
        
        results[`config-${config.name}`] = {
          success,
          statusCode: response.status,
          message: `${response.statusText} - ${responseText.substring(0, 50)}${responseText.length > 50 ? '...' : ''}`,
          time
        };
      } else {
        // Usar axios com configuração personalizada
        const result = await axios.get(config.route, {
          timeout: 5000,
          withCredentials: config.config.withCredentials !== false,
          headers: {
            ...config.config.headers,
            'X-Test-Config': config.name
          }
        }).then(response => ({
          success: true,
          statusCode: response.status,
          message: `OK (${response.statusText})`,
          time: 0
        })).catch(error => ({
          success: false,
          statusCode: error.response?.status,
          message: error.message,
          time: 0
        }));
        
        results[`config-${config.name}`] = result;
      }
    } catch (err) {
      console.error(`Erro em configuração ${config.name}:`, err);
      results[`config-${config.name}`] = { 
        success: false, 
        message: 'Erro: ' + (err instanceof Error ? err.message : String(err)),
        time: 0
      };
    }
  }
  
  // Verificar resultados
  const workingRoutes = Object.entries(results)
    .filter(([_, result]) => result.success)
    .map(([key]) => key);
  
  const gatewayErrors = Object.entries(results)
    .filter(([_, result]) => result.statusCode === 502)
    .map(([key]) => key);
  
  const timeoutErrors = Object.entries(results)
    .filter(([_, result]) => result.message?.includes('Timeout'))
    .map(([key]) => key);
  
  // Criar sumário e recomendações
  let summary = '';
  
  if (workingRoutes.length > 0) {
    summary = `✅ Rotas funcionando: ${workingRoutes.join(', ')}. `;
    
    // Recomendar a melhor rota para usar
    const bestRoute = workingRoutes[0];
    recommendations.push(`Use a rota "${bestRoute}" para comunicação com o servidor de autenticação.`);
  } else if (gatewayErrors.length > 0) {
    summary = `❌ Erro de Gateway (502) em: ${gatewayErrors.join(', ')}. `;
    recommendations.push('Verifique se o contêiner do NGINX está encaminhando corretamente as requisições para ms-auth:5000.');
    recommendations.push('Confirme que o serviço auth está escutando na porta correta dentro do contêiner.');
    recommendations.push('Verifique se há regras de firewall bloqueando a comunicação entre contêineres.');
  } else if (timeoutErrors.length > 0) {
    summary = `⚠️ Timeouts em: ${timeoutErrors.join(', ')}. `;
    recommendations.push('Aumente os valores de timeout no NGINX e no cliente Axios.');
    recommendations.push('Verifique se o serviço está sobrecarregado ou lento para responder.');
  } else {
    summary = '❌ Nenhuma rota está funcionando corretamente.';
    recommendations.push('Verifique os logs do NGINX e ms-auth para identificar potenciais erros.');
    recommendations.push('Reinicie os contêineres de NGINX e ms-auth.');
    recommendations.push('Verifique se há conflitos de porta ou configuração incorreta de rede no Docker.');
  }
  
  return {
    summary,
    routes: results,
    recommendations
  };
};

export default {
  checkAuthConnection,
  tryConnectWithRetry,
  diagnosticAuth
}; 