export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
  preferences?: UserPreferences;
  subscription?: UserSubscription;
}

export interface UserPreferences {
  objectives: string[];
  bibleExperienceLevel: 'beginner' | 'intermediate' | 'advanced';
  contentPreferences: ('text' | 'audio' | 'video')[];
  preferredTime: 'morning' | 'afternoon' | 'evening';
  onboardingCompleted: boolean;
}

export interface UserSubscription {
  id: string;
  userId: string;
  planType: 'free' | 'monthly' | 'annual';
  status: 'active' | 'inactive' | 'canceled';
  paymentGateway: 'stripe' | 'hotmart';
  expirationDate: string;
  createdAt: string;
}

export interface AuthResponse {
  user: User;
  tokens: {
    accessToken: string;
    refreshToken: string;
  };
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData extends LoginCredentials {
  name: string;
}

export interface ResetPasswordData {
  email: string;
  token: string;
  newPassword: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  resetPassword: (data: ResetPasswordData) => Promise<void>;
  updateUser: (user: User) => void;
} 
