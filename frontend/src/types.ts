export interface Habit {
  habit_id: number;
  name: string;
  frequency: 'daily' | 'weekly';
  creation_date: string;
}

export interface HabitStats {
  streak: number;
  completion_rate: number;
  total_completions: number;
}

export interface HabitRecord {
  record_id: number;
  habit_id: number;
  completion_time: string;
}

