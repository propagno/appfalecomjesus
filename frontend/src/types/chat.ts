export interface ChatMessage {
  id: string;
  userId: string;
  message: string;
  response: string;
  modelUsed: string;
  createdAt: string;
  context?: {
    studyId?: string;
    bibleReference?: string;
    reflectionId?: string;
  };
}

export interface ChatHistory {
  messages: ChatMessage[];
  hasMore: boolean;
  nextCursor?: string;
}

export interface ChatLimits {
  daily: {
    limit: number;
    remaining: number;
    reset: string;
  };
  premium: boolean;
}

export interface ChatPrompt {
  message: string;
  context?: {
    studyId?: string;
    bibleReference?: string;
    reflectionId?: string;
    userPreferences?: {
      bibleExperienceLevel: string;
      objectives: string[];
    };
  };
}

export interface ChatResponse {
  message: ChatMessage;
  limits: ChatLimits;
}

export interface ChatError {
  code: string;
  message: string;
  details?: {
    retryAfter?: number;
    limit?: number;
    remaining?: number;
    reset?: string;
  };
}

export interface ChatFilters {
  startDate?: string;
  endDate?: string;
  search?: string;
  context?: {
    studyId?: string;
    bibleReference?: string;
  };
} 
