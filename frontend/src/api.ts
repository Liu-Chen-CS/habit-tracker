import axios from 'axios';
import type { Habit, HabitStats, HabitRecord } from './types';

const API_BASE = 'http://127.0.0.1:5000/api';

export const api = {
  getHabits: () => axios.get<Habit[]>(`${API_BASE}/habits`),
  createHabit: (name: string, frequency: string) => 
    axios.post(`${API_BASE}/habits`, { name, frequency }),
  deleteHabit: (id: number) => axios.delete(`${API_BASE}/habits/${id}`),
  completeHabit: (id: number) => axios.post(`${API_BASE}/habits/${id}/complete`),
  getStats: (id: number) => axios.get<HabitStats>(`${API_BASE}/habits/${id}/stats`),
  getRecords: (id: number) => axios.get<HabitRecord[]>(`${API_BASE}/habits/${id}/records`)
};

