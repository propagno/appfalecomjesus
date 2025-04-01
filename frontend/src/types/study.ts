export interface Study {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  durationDays: number;
  imageUrl?: string;
  createdAt: string;
  sections: StudySection[];
}

export interface StudySection {
  id: string;
  studyPlanId: string;
  title: string;
  position: number;
  durationMinutes: number;
  content: StudyContent[];
}

export interface StudyContent {
  id: string;
  sectionId: string;
  contentType: 'text' | 'audio' | 'video';
  content: string;
  position: number;
  bibleReference?: {
    book: string;
    chapter: number;
    verse: number;
  };
}

export interface UserStudyProgress {
  id: string;
  userId: string;
  studyPlanId: string;
  currentSectionId: string;
  completionPercentage: number;
  startedAt: string;
  completedAt?: string;
}

export interface Reflection {
  id: string;
  userId: string;
  studySectionId: string;
  reflectionText: string;
  createdAt: string;
  studyTitle?: string;
  bibleVerse?: string;
}

export interface StudyFilters {
  category?: string;
  difficulty?: Study['difficulty'];
  search?: string;
  completed?: boolean;
}

export interface StudyPreferences {
  objectives: string[];
  bibleExperienceLevel: Study['difficulty'];
  contentPreferences: StudyContent['contentType'][];
  preferredTime: 'morning' | 'afternoon' | 'evening';
} 
