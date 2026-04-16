#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}Starting PatentMine...${NC}\n"

# Kill any existing processes on ports 8000 and 8501
echo -e "${YELLOW}Clearing ports 8000 and 8501...${NC}"
fuser -k 8000/tcp 2>/dev/null
fuser -k 8501/tcp 2>/dev/null
sleep 1

# Start FastAPI backend using system python3
echo "Starting Backend API (Port 8000)..."
/usr/bin/python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
API_PID=$!

# Wait briefly for API to start
sleep 2

# Start Streamlit frontend using system python3
echo "Starting Frontend Dashboard (Port 8501)..."
/usr/bin/python3 -m streamlit run ui/app.py --server.port 8501 --browser.gatherUsageStats false > frontend.log 2>&1 &
UI_PID=$!

# Wait for streamlit to spin up then open browser
sleep 3
xdg-open http://localhost:8501 2>/dev/null || echo ""

function cleanup() {
    echo -e "\n${CYAN}Shutting down PatentMine...${NC}"
    kill $API_PID 2>/dev/null
    kill $UI_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo -e "\n${GREEN}PatentMine is running!${NC}"
echo -e "  → Open in browser: ${GREEN}http://localhost:8501${NC}"
echo -e "\nPress [Ctrl+C] to shut down.\n"

wait $API_PID $UI_PID
