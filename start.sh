#!/bin/bash

echo "=================================="
echo "🚀 Starting Habit Tracker"
echo "=================================="
echo ""

# Check if port is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Backend port 5000 is already in use"
    echo "Please close the running backend service or use a different port"
    exit 1
fi

# Start backend
echo "📊 Starting backend service..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Check if backend started successfully
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Start frontend
echo "🎨 Starting frontend service..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=================================="
echo "✅ Services started successfully!"
echo "=================================="
echo ""
echo "📍 Backend URL: http://127.0.0.1:5000"
echo "📍 Frontend URL: http://localhost:5173"
echo ""
echo "⚠️  Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
wait
