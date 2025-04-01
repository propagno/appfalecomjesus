export interface UserPoints {
  id: string;
  userId: string;
  totalPoints: number;
  weeklyPoints: number;
  monthlyPoints: number;
  lastUpdated: string;
}

export interface Achievement {
  id: string;
  userId: string;
  badgeName: string;
  description: string;
  imageUrl: string;
  earnedAt: string;
  category: 'study' | 'chat' | 'reflection' | 'bible' | 'special';
  requirements: {
    type: string;
    value: number;
    current: number;
  };
}

export interface Certificate {
  id: string;
  userId: string;
  studyPlanId: string;
  completionDate: string;
  certificateCode: string;
  downloadCount: number;
  imageUrl: string;
  studyTitle: string;
  bibleVerse?: string;
  customMessage?: string;
}

export interface AdReward {
  id: string;
  userId: string;
  messageBonus: number;
  adProvider: string;
  watchedAt: string;
}

export interface GamificationProgress {
  points: UserPoints;
  achievements: Achievement[];
  certificates: Certificate[];
  nextAchievements: Achievement[];
  weeklyRank?: number;
  monthlyRank?: number;
}

export interface GamificationEvent {
  type: 'study_completed' | 'reflection_added' | 'chat_used' | 'bible_read' | 'ad_watched';
  userId: string;
  points: number;
  metadata?: Record<string, unknown>;
  timestamp: string;
}

export interface GamificationFilters {
  category?: Achievement['category'];
  startDate?: string;
  endDate?: string;
  earned?: boolean;
} 
