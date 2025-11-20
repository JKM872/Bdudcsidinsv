# 🚀 Quick Start Guide - Dashboard

## Prerequisites
- Python 3.8+ (already installed)
- Node.js 18+ (need to install)
- Running Supabase database (already configured)

## 1. Install Node.js

Download and install from: https://nodejs.org/
```bash
# Verify installation
node --version
npm --version
```

## 2. Install Dependencies

### Backend (Already Done)
```bash
pip install flask flask-cors
```

### Frontend
```bash
cd c:\Users\jakub\Desktop\BigOne\dashboard
npm install
```

## 3. Start Servers

### Terminal 1 - Backend API
```bash
cd c:\Users\jakub\Desktop\BigOne
python api/app.py
```

Expected output:
```
🚀 Starting Sports Prediction API Server...
📊 Dashboard: http://localhost:5000
🔍 API Docs: http://localhost:5000/api/health
 * Running on http://0.0.0.0:5000
```

### Terminal 2 - Frontend Dashboard
```bash
cd c:\Users\jakub\Desktop\BigOne\dashboard
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

## 4. Access Dashboard

Open browser: **http://localhost:3000**

## 5. Populate Data (If Empty)

```bash
# Run scraper with all sources
python livesport_h2h_scraper.py \
  --mode auto \
  --date 2025-11-18 \
  --sports football \
  --use-forebet \
  --use-gemini \
  --use-sofascore \
  --use-supabase \
  --headless
```

## 6. Test API

```bash
# Health check
curl http://localhost:5000/api/health

# Get predictions
curl http://localhost:5000/api/predictions/recent?days=7

# Get accuracy
curl http://localhost:5000/api/accuracy?days=30
```

## Dashboard Features

### 📊 Stats Overview
- Total predictions, qualified picks, success rate
- Visual cards with icons

### 🔐 Consensus Picks
- Top 5 picks with 3-4 sources agreeing
- LOCK/HIGH/MEDIUM badges
- Source agreement visualization

### 📈 Accuracy Chart
- Bar chart comparing all 4 sources
- Accuracy percentages
- Total and correct predictions

### 📋 Predictions Table
- Full list with filters
- Sort by date, sport, consensus
- Individual source predictions

## Filters

- **Time Period**: Today, 7, 14, 30 days
- **Sport**: All, Football, Basketball, Volleyball, Tennis

## Troubleshooting

### Port 5000 already in use
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Port 3000 already in use
```bash
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### No data displayed
- Run scraper to populate Supabase
- Check API is running: http://localhost:5000/api/health

### CORS errors
- Verify both servers are running
- Check Vite proxy in dashboard/vite.config.js

---

**Ready to use!** 🎉
