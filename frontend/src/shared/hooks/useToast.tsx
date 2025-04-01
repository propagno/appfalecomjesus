import { toast, ToastOptions } from 'react-hot-toast';

/**
 * Hook para fornecer notificações toast com configurações padrão
 */
export const useToast = () => {
  const defaultOptions: ToastOptions = {
    duration: 5000,
    position: 'top-right',
  };

  return {
    success: (message: string, options?: ToastOptions) => toast.success(message, { ...defaultOptions, ...options }),
    error: (message: string, options?: ToastOptions) => toast.error(message, { ...defaultOptions, ...options }),
    info: (message: string, options?: ToastOptions) => toast(message, { ...defaultOptions, ...options }),
    warning: (message: string, options?: ToastOptions) => toast(message, { ...defaultOptions, icon: '⚠️', ...options }),
    promise: toast.promise,
    dismiss: toast.dismiss,
    custom: toast,
  };
};

export default useToast; 