# ⚡ Quick Start Guide

## 🎯 First Time Here? Follow Along!

### Method 1: One-Click Start (Recommended)

```bash
./start.sh
```

That's it! The script will automatically start both backend and frontend.

---

### Method 2: Manual Start (Step-by-Step)

#### Step 1: Start Backend (Terminal 1)

```bash
cd /Users/liu.chen/habbit/backend
python3 app.py
```

Success when you see:
```
============================================================
🚀 Habit Tracker API Starting
📊 Database: habit_tracker.db
🌐 API URL: http://127.0.0.1:5000
============================================================
```

#### Step 2: Start Frontend (Terminal 2)

Open a new terminal window:

```bash
cd /Users/liu.chen/habbit/frontend
npm run dev
```

Success when you see Vite startup info:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

---

## 🎮 Start Using

1. Open browser and visit: `http://localhost:5173`
2. Add your first habit (e.g., "Read for 30 minutes daily")
3. Click "✓ Complete" button to mark as done
4. Watch your streak count and completion rate grow

---

## 🔧 Test API is Working

```bash
# Test get habits list
curl http://127.0.0.1:5000/api/habits

# Should return: [] (empty array)
```

---

## ❌ Troubleshooting

### Issue 1: pip command not found
```bash
# Use pip3 instead
pip3 install -r requirements.txt

# Or
python3 -m pip install -r requirements.txt
```

### Issue 2: Port already in use
```bash
# Check processes using the ports
lsof -i :5000
lsof -i :5173

# Kill the process
kill -9 <PID>
```

### Issue 3: Frontend can't connect to backend
- ✅ Confirm backend is running (visit http://127.0.0.1:5000/api/habits)
- ✅ Check console for CORS errors
- ✅ Confirm backend code has `CORS(app)`

### Issue 4: axios not installed
```bash
cd frontend
npm install axios
```

---

## 📝 Development Tips

### Recommended Development Tools
- **Editor**: VS Code
- **Python Plugins**: Python, Pylance
- **React Plugins**: ES7+ React/Redux/React-Native snippets
- **Browser Plugin**: React Developer Tools

### View Logs
- **Backend logs**: Check Terminal 1 output
- **Frontend logs**: Open browser DevTools (F12)

### Database Location
- Data stored in: `backend/habit_tracker.db`
- Use DB Browser for SQLite to visualize

---

## 🎉 Done!

Now you can:
- ✅ Add habits
- ✅ Mark as complete
- ✅ View statistics
- ✅ Delete habits

Happy habit building! 💪

---

**Questions?** Check the full documentation: [README.md](README.md)
