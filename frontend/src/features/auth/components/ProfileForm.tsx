import React, { useState, useRef } from 'react';
import { useAuthContext } from '../contexts/AuthContext';
import { toast } from 'react-hot-toast';
import { ProfileUpdateData, User } from '../types';
import Button from '../../../shared/components/ui/Button';
import Input from '../../../shared/components/ui/Input';

// Ícones inline
const UserIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const EmailIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>
);

const LockIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
  </svg>
);

const KeyIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
  </svg>
);

interface ProfileFormProps {
  user: User;
  onSuccess?: () => void;
}

/**
 * Formulário de atualização de perfil
 */
const ProfileForm: React.FC<ProfileFormProps> = ({ user, onSuccess }) => {
  const { updateProfile, isUpdatingProfile } = useAuthContext();
  const [formData, setFormData] = useState<ProfileUpdateData>({
    name: user.name || '',
    email: user.email || '',
    password: '',
    password_confirmation: '',
    current_password: ''
  });
  const [avatar, setAvatar] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(user.avatar_url || null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Manipula mudanças nos inputs
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    
    // Remove erro ao digitar no campo
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };
  
  // Manipula seleção de avatar
  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      
      // Verifica tamanho (máx 2MB)
      if (file.size > 2 * 1024 * 1024) {
        setErrors({ avatar: 'A imagem deve ter no máximo 2MB' });
        return;
      }
      
      // Cria preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatarPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      
      setAvatar(file);
      
      // Remove erro
      if (errors.avatar) {
        setErrors((prev) => {
          const newErrors = { ...prev };
          delete newErrors.avatar;
          return newErrors;
        });
      }
    }
  };
  
  // Abre o seletor de arquivo
  const handleAvatarClick = () => {
    fileInputRef.current?.click();
  };
  
  // Valida o formulário
  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    // Validar nome
    if (!formData.name?.trim()) {
      newErrors.name = 'O nome é obrigatório';
    }
    
    // Validar email
    if (!formData.email?.trim()) {
      newErrors.email = 'O e-mail é obrigatório';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Insira um e-mail válido';
    }
    
    // Validar senha (apenas se estiver alterando)
    if (formData.password) {
      if (formData.password.length < 6) {
        newErrors.password = 'A senha deve ter no mínimo 6 caracteres';
      }
      
      if (formData.password !== formData.password_confirmation) {
        newErrors.password_confirmation = 'As senhas não coincidem';
      }
      
      if (!formData.current_password) {
        newErrors.current_password = 'Informe sua senha atual para confirmar as alterações';
      }
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  // Manipula o envio do formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    try {
      const updateData: ProfileUpdateData = {
        name: formData.name,
        email: formData.email
      };
      
      // Apenas incluir senha se foi preenchida
      if (formData.password) {
        updateData.password = formData.password;
        updateData.password_confirmation = formData.password_confirmation;
        updateData.current_password = formData.current_password;
      }
      
      // Incluir avatar se foi selecionado
      if (avatar) {
        updateData.avatar = avatar;
      }

      // Enviar atualização
      await updateProfile(updateData);
      
      // Handle success
      toast.success('Perfil atualizado com sucesso!');
      // Limpar senhas após sucesso
      setFormData((prev) => ({
        ...prev,
        password: '',
        password_confirmation: '',
        current_password: ''
      }));
      
      if (onSuccess) {
        onSuccess();
      }
      
      // Esconde mensagem de sucesso após alguns segundos
      setTimeout(() => {
        setSuccess(false);
      }, 5000);
    } catch (error: any) {
      // Handle error
      if (error.response?.data?.errors) {
        // Converter erros de array para string
        const formattedErrors: Record<string, string> = {};
        Object.entries(error.response.data.errors).forEach(([key, value]) => {
          if (Array.isArray(value)) {
            formattedErrors[key] = value[0];
          } else if (typeof value === 'string') {
            formattedErrors[key] = value;
          }
        });
        setErrors(formattedErrors);
      } else {
        toast.error('Erro ao atualizar perfil. Tente novamente.');
      }
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {errors.general && (
        <div className="mb-6 p-3 bg-spirit-red-400/10 text-spirit-red-600 rounded-md border border-spirit-red-400/20 font-body">
          {errors.general}
        </div>
      )}
      
      {success && (
        <div className="mb-6 p-3 bg-spirit-green-400/10 text-spirit-green-600 rounded-md border border-spirit-green-400/20 font-body">
          <p className="font-medium font-heading">Perfil atualizado com sucesso!</p>
        </div>
      )}
      
      <div className="flex flex-col items-center mb-6">
        <div 
          className="w-24 h-24 rounded-full bg-spirit-earth-100 flex items-center justify-center overflow-hidden cursor-pointer border-2 border-spirit-earth-200 hover:border-spirit-blue-500 transition-colors"
          onClick={handleAvatarClick}
        >
          {avatarPreview ? (
            <img 
              src={avatarPreview} 
              alt={`Avatar de ${formData.name}`} 
              className="w-full h-full object-cover" 
            />
          ) : (
            <span className="text-spirit-blue-500 text-4xl font-heading">{formData.name?.[0]?.toUpperCase() || 'U'}</span>
          )}
        </div>
        
        <input
          type="file"
          id="avatar"
          name="avatar"
          accept="image/*"
          className="hidden"
          onChange={handleAvatarChange}
          ref={fileInputRef}
        />
        
        <Button
          type="button"
          variant="ghost"
          size="sm"
          onClick={handleAvatarClick}
          className="mt-2"
        >
          Alterar foto
        </Button>
        
        {errors.avatar && (
          <p className="mt-1 text-sm text-spirit-red-500 font-body">{errors.avatar}</p>
        )}
      </div>
      
      <div className="space-y-5">
        <Input
          label="Nome completo"
          id="name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
          leftIcon={<UserIcon />}
          error={errors.name}
          fullWidth
        />
        
        <Input
          label="E-mail"
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          leftIcon={<EmailIcon />}
          error={errors.email}
          fullWidth
        />
        
        <div className="pt-4 border-t border-spirit-earth-100">
          <h3 className="text-lg font-medium text-spirit-blue-700 font-heading mb-4">Alterar senha</h3>
          
          <div className="space-y-5">
            <Input
              label="Nova senha"
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              leftIcon={<LockIcon />}
              error={errors.password}
              helperText="Deixe em branco para manter a senha atual"
              fullWidth
            />
            
            <Input
              label="Confirmar nova senha"
              id="password_confirmation"
              name="password_confirmation"
              type="password"
              value={formData.password_confirmation}
              onChange={handleChange}
              error={errors.password_confirmation}
              fullWidth
            />
            
            <Input
              label="Senha atual"
              id="current_password"
              name="current_password"
              type="password"
              value={formData.current_password}
              onChange={handleChange}
              leftIcon={<KeyIcon />}
              error={errors.current_password}
              helperText="Necessário para confirmar as alterações"
              fullWidth
            />
          </div>
        </div>
      </div>
      
      <div className="flex items-center justify-end pt-5">
        <Button
          type="submit"
          disabled={isUpdatingProfile}
          size="lg"
        >
          {isUpdatingProfile ? 'Salvando...' : 'Salvar alterações'}
        </Button>
      </div>
    </form>
  );
};

export default ProfileForm; 