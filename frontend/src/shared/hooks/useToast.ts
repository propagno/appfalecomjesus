/**
 * Hook personalizado para utilizar o sistema de notificações Toast
 */
import { toast, ToastOptions } from 'react-toastify';

// Opções padrão para os toasts
const defaultOptions: ToastOptions = {
  position: 'top-right',
  autoClose: 4000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
};

interface ToastHook {
  success: (message: string, options?: ToastOptions) => void;
  error: (message: string, options?: ToastOptions) => void;
  info: (message: string, options?: ToastOptions) => void;
  warning: (message: string, options?: ToastOptions) => void;
  dismiss: (id?: string | number) => void;
  dismissAll: () => void;
}

/**
 * Hook para exibir notificações toast
 */
export const useToast = (): ToastHook => {
  return {
    /**
     * Exibe uma mensagem de sucesso
     * @param message Mensagem a ser exibida
     * @param options Opções adicionais para o toast
     */
    success: (message: string, options?: ToastOptions) => {
      toast.success(message, { ...defaultOptions, ...options });
    },

    /**
     * Exibe uma mensagem de erro
     * @param message Mensagem a ser exibida
     * @param options Opções adicionais para o toast
     */
    error: (message: string, options?: ToastOptions) => {
      toast.error(message, { ...defaultOptions, ...options });
    },

    /**
     * Exibe uma mensagem informativa
     * @param message Mensagem a ser exibida
     * @param options Opções adicionais para o toast
     */
    info: (message: string, options?: ToastOptions) => {
      toast.info(message, { ...defaultOptions, ...options });
    },

    /**
     * Exibe uma mensagem de alerta/aviso
     * @param message Mensagem a ser exibida
     * @param options Opções adicionais para o toast
     */
    warning: (message: string, options?: ToastOptions) => {
      toast.warning(message, { ...defaultOptions, ...options });
    },

    /**
     * Remove um toast específico pelo ID
     * @param id ID do toast a ser removido
     */
    dismiss: (id?: string | number) => {
      if (id) {
        toast.dismiss(id);
      } else {
        toast.dismiss();
      }
    },

    /**
     * Remove todos os toasts ativos
     */
    dismissAll: () => {
      toast.dismiss();
    },
  };
};

export default useToast; 