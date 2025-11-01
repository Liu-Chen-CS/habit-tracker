import React, { useState, useEffect } from 'react';
import { api } from './api';
import type { Habit, HabitStats } from './types';
import './App.css';

const App: React.FC = () => {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [stats, setStats] = useState<Map<number, HabitStats>>(new Map());
  const [newHabitName, setNewHabitName] = useState('');
  const [newHabitFreq, setNewHabitFreq] = useState<'daily' | 'weekly'>('daily');
  const [loading, setLoading] = useState(false);

  const loadHabits = async () => {
    try {
      setLoading(true);
      const res = await api.getHabits();
      setHabits(res.data);
      
      // Load statistics for each habit
      const statsMap = new Map<number, HabitStats>();
      for (const habit of res.data) {
        const statsRes = await api.getStats(habit.habit_id);
        statsMap.set(habit.habit_id, statsRes.data);
      }
      setStats(statsMap);
    } catch (error) {
      console.error('Failed to load habits:', error);
      alert('Unable to connect to backend service. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHabits();
  }, []);

  const handleAddHabit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newHabitName.trim()) return;
    
    try {
      await api.createHabit(newHabitName, newHabitFreq);
      setNewHabitName('');
      loadHabits();
    } catch (error) {
      console.error('Failed to create habit:', error);
      alert('Failed to create habit');
    }
  };

  const handleComplete = async (id: number) => {
    try {
      await api.completeHabit(id);
      loadHabits();
    } catch (error) {
      console.error('Failed to mark as complete:', error);
      alert('Failed to mark as complete');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this habit?')) {
      try {
        await api.deleteHabit(id);
        loadHabits();
      } catch (error) {
        console.error('Failed to delete habit:', error);
        alert('Failed to delete habit');
      }
    }
  };

  return (
    <>
      <div className="app">
        <div className="container">
          <h1>Habit Tracker</h1>
        
        <div className="add-section">
          <h2>Add New Habit</h2>
          <form onSubmit={handleAddHabit}>
            <input
              type="text"
              value={newHabitName}
              onChange={(e) => setNewHabitName(e.target.value)}
              placeholder="e.g., Read for 30 minutes daily"
            />
            <select value={newHabitFreq} onChange={(e) => setNewHabitFreq(e.target.value as any)}>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
            </select>
            <button type="submit">➕ Add</button>
          </form>
        </div>

        <h2>My Habits</h2>
        {loading ? (
          <div className="empty-state">
            <p>Loading...</p>
          </div>
        ) : habits.length === 0 ? (
          <div className="empty-state">
            <p>No habits yet. Add one to get started!</p>
          </div>
        ) : (
          <div className="habit-list">
            {habits.map(habit => {
              const habitStats = stats.get(habit.habit_id);
              return (
                <div key={habit.habit_id} className="habit-card">
                  <div className="habit-info">
                    <h3>{habit.name}</h3>
                    <div className="habit-meta">
                      Frequency: {habit.frequency === 'daily' ? 'Daily' : 'Weekly'} | 
                      Streak: <span className="streak">{habitStats?.streak || 0} days</span> | 
                      Completion: {habitStats?.completion_rate.toFixed(1) || 0}%
                    </div>
                  </div>
                  <div className="habit-actions">
                    <button className="btn-complete" onClick={() => handleComplete(habit.habit_id)}>
                      ✓ Complete
                    </button>
                    <button className="btn-delete" onClick={() => handleDelete(habit.habit_id)}>
                      🗑️
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
        </div>
      </div>
      
      <div className="author-info">
        <div className="author-title">Student Information</div>
        <p><span className="label">Student:</span> Liu Chen</p>
        <p><span className="label">Matriculation no:</span> 102302879</p>
        <p><span className="label">Course:</span> DLBDSOOFPP01</p>
      </div>
    </>
  );
};

export default App;
