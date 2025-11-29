# Habit Tracker

A modern habit tracking application built with Flask + React + TypeScript.

## Project Structure

```
habbit/
├── backend/              # Flask backend
│   ├── app.py           # Main application file
│   ├── requirements.txt # Python dependencies
│   └── habit_tracker.db # SQLite database (auto-generated)
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.tsx     # Main component
│   │   ├── App.css     # Styles
│   │   ├── api.ts      # API calls
│   │   └── types.ts    # TypeScript types
│   └── package.json
└── README.md
```

## Quick Start

### Start Backend (Flask)

```bash
# Navigate to backend directory
cd backend

# Install dependencies (if not already installed)
pip3 install -r requirements.txt

# Start backend server
python3 app.py
```

Backend will start at `http://127.0.0.1:5000`

### Start Frontend (React)

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install axios

# Start development server
npm run dev
```

Frontend will start at `http://localhost:5173`

## Features

- Add habits (daily/weekly)
- Mark as complete
- Track consecutive day streaks
- Calculate completion rate
- Delete habits
- Beautiful modern UI
- Complete error handling

## How to Use

1. **Add Habit**: Enter habit name in the "Add New Habit" section, select frequency, and click Add
2. **Mark Complete**: Click the "✓ Complete" button to mark today as done
3. **View Stats**: Each habit card displays streak count and completion rate
4. **Delete Habit**: Click the "🗑️" button to delete (confirmation required)

## API Endpoints

| Method | Endpoint | Function |
|--------|----------|----------|
| GET | `/api/habits` | Get all habits |
| POST | `/api/habits` | Create new habit |
| DELETE | `/api/habits/<id>` | Delete habit |
| POST | `/api/habits/<id>/complete` | Mark as complete |
| GET | `/api/habits/<id>/stats` | Get statistics |
| GET | `/api/habits/<id>/records` | Get completion records |

## Tech Stack

**Backend:**
- Python 3.9+
- Flask 3.1.2
- Flask-CORS 6.0.1
- SQLite 3

**Frontend:**
- React 18
- TypeScript
- Vite
- Axios
