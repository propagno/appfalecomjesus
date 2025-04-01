import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

// Obtenha a URL base da API das variáveis de ambiente
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Crie a instância do axios com configurações padrão
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Necessário para enviar/receber cookies (JWT)
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Tratamento centralizado de erros
export const handleApiError = (error: AxiosError): never => {
  // Extrair a mensagem de erro
  let errorMessage = 'Ocorreu um erro inesperado';
  
  if (error.response) {
    // O servidor respondeu com status de erro
    const data = error.response.data as any;
    errorMessage = data.message || `Erro ${error.response.status}: ${error.response.statusText}`;
    
    // Se for erro 401 (não autorizado), pode disparar ação para logout
    if (error.response.status === 401) {
      // Pode disparar um evento para logout ou redirecionamento
      console.error('Sessão expirada ou inválida');
    }
  } else if (error.request) {
    // A requisição foi feita mas não houve resposta
    errorMessage = 'Não foi possível conectar ao servidor';
  }
  
  // Lança o erro com a mensagem formatada
  throw new Error(errorMessage);
};

// Configurar interceptadores para refreshToken, etc.
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Se receber 401 (Unauthorized) e não for uma tentativa de refresh
    if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('auth/refresh')) {
      originalRequest._retry = true;
      
      try {
        // Tentar refrescar o token
        await axios.post(`${API_BASE_URL}/auth/refresh`, {}, { withCredentials: true });
        
        // Retentar a requisição original
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // Se falhar no refresh, propagar o erro
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  },
);

// Interceptor de requisição - adiciona headers customizados, tokens, etc.
axiosInstance.interceptors.request.use(
  (config) => {
    // Aqui podemos adicionar headers dinâmicos ou lógica antes da requisição
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Funções do cliente API
const apiClient = {
  get: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    try {
      const response: AxiosResponse<T> = await axiosInstance.get(url, config);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
  
  post: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    try {
      const response: AxiosResponse<T> = await axiosInstance.post(url, data, config);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
  
  put: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    try {
      const response: AxiosResponse<T> = await axiosInstance.put(url, data, config);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
  
  patch: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    try {
      const response: AxiosResponse<T> = await axiosInstance.patch(url, data, config);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
  
  delete: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    try {
      const response: AxiosResponse<T> = await axiosInstance.delete(url, config);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
  
  // Método para enviar dados como form-urlencoded (útil para algumas APIs)
  postForm: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    try {
      const formData = new URLSearchParams();
      
      // Converter objeto para formato form-urlencoded
      if (data) {
        Object.entries(data).forEach(([key, value]) => {
          formData.append(key, String(value));
        });
      }
      
      const response: AxiosResponse<T> = await axiosInstance.post(url, formData, {
        ...config,
        headers: {
          ...config?.headers,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
  
  // Acesso à instância direta do axios (caso necessário)
  axios: axiosInstance,
};

export default apiClient; 