"""
Habit Tracker Backend API
Python + Flask + SQLite + CORS
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from flask import Flask, request, jsonify
from flask_cors import CORS

# ============================================================
# 1. Core Data Models
# ============================================================

class Habit:
    """Habit definition class"""
    
    def __init__(self, habit_id: Optional[int], name: str, frequency: str, 
                 creation_date: Optional[datetime] = None):
        self.habit_id = habit_id
        self.name = name
        self.frequency = frequency
        self.creation_date = creation_date or datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'habit_id': self.habit_id,
            'name': self.name,
            'frequency': self.frequency,
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        }


class HabitRecord:
    """Habit completion record class"""
    
    def __init__(self, record_id: Optional[int], habit_id: int, 
                 completion_time: Optional[datetime] = None):
        self.record_id = record_id
        self.habit_id = habit_id
        self.completion_time = completion_time or datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'record_id': self.record_id,
            'habit_id': self.habit_id,
            'completion_time': self.completion_time.strftime('%Y-%m-%d %H:%M:%S')
        }


# ============================================================
# 2. Database Manager
# ============================================================

class DatabaseManager:
    """SQLite database management"""
    
    def __init__(self, db_path: str = 'habit_tracker.db'):
        self.db_path = db_path
        self.initialize_db()
    
    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_db(self):
        """Initialize database tables"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT NOT NULL,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES Habits(habit_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_habit(self, habit: Habit) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Habits (name, frequency, creation_date) VALUES (?, ?, ?)',
            (habit.name, habit.frequency, habit.creation_date)
        )
        habit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return habit_id
    
    def log_completion(self, record: HabitRecord) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Records (habit_id, completion_time) VALUES (?, ?)',
            (record.habit_id, record.completion_time)
        )
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return record_id
    
    def get_all_habits(self) -> List[Habit]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Habits ORDER BY creation_date DESC')
        rows = cursor.fetchall()
        conn.close()
        
        habits = []
        for row in rows:
            # Handle both formats: with and without microseconds
            date_str = row['creation_date']
            try:
                creation_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                creation_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            
            habit = Habit(
                habit_id=row['habit_id'],
                name=row['name'],
                frequency=row['frequency'],
                creation_date=creation_date
            )
            habits.append(habit)
        return habits
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Habits WHERE habit_id = ?', (habit_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Handle both formats: with and without microseconds
            date_str = row['creation_date']
            try:
                creation_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                creation_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            
            return Habit(
                habit_id=row['habit_id'],
                name=row['name'],
                frequency=row['frequency'],
                creation_date=creation_date
            )
        return None
    
    def get_records_by_habit(self, habit_id: int) -> List[HabitRecord]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Records WHERE habit_id = ? ORDER BY completion_time DESC',
            (habit_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            # Handle both formats: with and without microseconds
            date_str = row['completion_time']
            try:
                completion_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                completion_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            
            record = HabitRecord(
                record_id=row['record_id'],
                habit_id=row['habit_id'],
                completion_time=completion_time
            )
            records.append(record)
        return records
    
    def delete_habit(self, habit_id: int) -> bool:
        """Delete habit and all its records"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Records WHERE habit_id = ?', (habit_id,))
        cursor.execute('DELETE FROM Habits WHERE habit_id = ?', (habit_id,))
        conn.commit()
        conn.close()
        return True
    
    def calculate_streak(self, habit_id: int) -> int:
        """Calculate consecutive days streak"""
        records = self.get_records_by_habit(habit_id)
        if not records:
            return 0
        
        completion_dates = sorted(set(
            r.completion_time.date() for r in records
        ), reverse=True)
        
        if not completion_dates:
            return 0
        
        today = datetime.now().date()
        if completion_dates[0] not in [today, today - timedelta(days=1)]:
            return 0
        
        streak = 1
        for i in range(len(completion_dates) - 1):
            diff = (completion_dates[i] - completion_dates[i + 1]).days
            if diff == 1:
                streak += 1
            else:
                break
        
        return streak
    
    def get_completion_rate(self, habit_id: int, days: int = 30) -> float:
        """Calculate completion rate"""
        start_date = datetime.now() - timedelta(days=days)
        records = self.get_records_by_habit(habit_id)
        recent_records = [r for r in records if r.completion_time >= start_date]
        completion_days = len(set(r.completion_time.date() for r in recent_records))
        return (completion_days / days) * 100 if days > 0 else 0.0


# ============================================================
# 3. Flask REST API
# ============================================================

app = Flask(__name__)
CORS(app)  # Enable CORS
db_manager = DatabaseManager()

@app.route('/api/habits', methods=['GET'])
def get_habits():
    """Get all habits"""
    habits = db_manager.get_all_habits()
    return jsonify([h.to_dict() for h in habits])

@app.route('/api/habits', methods=['POST'])
def create_habit():
    """Create new habit"""
    data = request.json
    habit = Habit(
        habit_id=None,
        name=data['name'],
        frequency=data['frequency']
    )
    habit_id = db_manager.add_habit(habit)
    return jsonify({'habit_id': habit_id, 'message': 'Created successfully'}), 201

@app.route('/api/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    """Delete habit"""
    db_manager.delete_habit(habit_id)
    return jsonify({'message': 'Deleted successfully'})

@app.route('/api/habits/<int:habit_id>/complete', methods=['POST'])
def complete_habit(habit_id):
    """Mark as complete"""
    record = HabitRecord(record_id=None, habit_id=habit_id)
    record_id = db_manager.log_completion(record)
    return jsonify({'record_id': record_id, 'message': 'Completed'})

@app.route('/api/habits/<int:habit_id>/stats', methods=['GET'])
def get_habit_stats(habit_id):
    """Get habit statistics"""
    streak = db_manager.calculate_streak(habit_id)
    completion_rate = db_manager.get_completion_rate(habit_id)
    records = db_manager.get_records_by_habit(habit_id)
    
    return jsonify({
        'streak': streak,
        'completion_rate': completion_rate,
        'total_completions': len(records)
    })

@app.route('/api/habits/<int:habit_id>/records', methods=['GET'])
def get_habit_records(habit_id):
    """Get completion records"""
    records = db_manager.get_records_by_habit(habit_id)
    return jsonify([r.to_dict() for r in records])

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Habit Tracker API Starting")
    print("📊 Database: habit_tracker.db")
    print("🌐 API URL: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
