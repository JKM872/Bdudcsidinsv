# Phase 7: Real-Time Dashboard

## Overview
Full-stack web dashboard for visualizing sports predictions with 4-source consensus analysis.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DASHBOARD STACK                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  FRONTEND (React + Vite)                                │
│  ├─ Port: 3000                                         │
│  ├─ TailwindCSS for styling                            │
│  ├─ Recharts for data visualization                    │
│  ├─ React Query for data fetching                      │
│  └─ Axios for API calls                                │
│                                                         │
│  BACKEND (Flask API)                                    │
│  ├─ Port: 5000                                         │
│  ├─ RESTful API endpoints                              │
│  ├─ CORS enabled                                       │
│  ├─ Supabase integration                               │
│  └─ Real-time data queries                             │
│                                                         │
│  DATABASE (Supabase PostgreSQL)                         │
│  ├─ Cloud-hosted                                       │
│  ├─ 32-column predictions table                        │
│  ├─ Row Level Security                                 │
│  └─ Indexed for performance                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Features

### 📊 Statistics Dashboard
- Total predictions count
- Qualified picks counter
- Predictions with results
- Success rate percentage
- Sport-by-sport breakdown

### 🔐 Consensus Picks Display
- Top 5 picks with 3-4 sources agreeing
- Visual badges (LOCK 🔐 / HIGH 🟢 / MEDIUM 🟡)
- Source agreement indicators
- Confidence percentages from all 4 sources

### 📈 Accuracy Tracking
- Bar chart comparing all 4 sources
- Historical accuracy percentages
- Total predictions per source
- Correct predictions count
- ROI calculations (future)

### 📋 Predictions Table
- Sortable, filterable match list
- Date/time display
- Match details (teams, sport, league)
- Consensus level badges
- Individual source predictions
- Result status (Pending/Complete)

### ⚙️ Filters
- Time period selector (Today, 7/14/30 days)
- Sport filter (All, Football, Basketball, Volleyball, Tennis)
- Real-time updates via React Query

## API Endpoints

### Health Check
```
GET /api/health
Response: {status, timestamp, version}
```

### Recent Predictions
```
GET /api/predictions/recent?days=7&sport=football&qualified=true
Response: {success, count, predictions[]}
```

### Statistics
```
GET /api/predictions/stats?days=30
Response: {total_predictions, qualified_predictions, by_sport{}}
```

### Accuracy
```
GET /api/accuracy?days=30
Response: {sources: {livesport: {accuracy, total, correct}, ...}}
```

### Consensus Picks
```
GET /api/consensus?days=7&min_agreement=3
Response: {picks[], count, min_agreement}
```

### Today's Predictions
```
GET /api/predictions/today
Response: {date, count, predictions[]}
```

### Upcoming Predictions
```
GET /api/predictions/upcoming
Response: {by_date: {'2025-11-19': [...], ...}, total_count}
```

### Prediction Detail
```
GET /api/predictions/<id>
Response: {success, prediction{}}
```

### Update Result
```
POST /api/predictions/<id>/result
Body: {actual_result: '1'/'X'/'2', home_score: int, away_score: int}
Response: {success, message}
```

## Installation

### Backend Setup
```bash
cd c:\Users\jakub\Desktop\BigOne

# Install Python dependencies (already in requirements.txt)
pip install flask flask-cors

# Run API server
python api/app.py
# API available at: http://localhost:5000
```

### Frontend Setup
```bash
cd c:\Users\jakub\Desktop\BigOne\dashboard

# Install Node.js dependencies
npm install

# Run development server
npm run dev
# Dashboard available at: http://localhost:3000
```

## Usage

### Start Both Servers
```bash
# Terminal 1 - Backend
cd c:\Users\jakub\Desktop\BigOne
python api/app.py

# Terminal 2 - Frontend
cd c:\Users\jakub\Desktop\BigOne\dashboard
npm run dev
```

### Access Dashboard
Open browser: http://localhost:3000

### Build for Production
```bash
cd dashboard
npm run build
# Output in: dashboard/dist/
```

## Components

### Frontend Structure
```
dashboard/
├── src/
│   ├── main.jsx              # Entry point
│   ├── App.jsx               # Main app component
│   ├── index.css             # Global styles + Tailwind
│   ├── api.js                # API client functions
│   └── components/
│       ├── Header.jsx        # Top navigation
│       ├── Dashboard.jsx     # Main dashboard container
│       ├── StatsOverview.jsx # 4 stat cards
│       ├── ConsensusPicks.jsx # Top consensus picks
│       ├── AccuracyChart.jsx  # Bar chart with Recharts
│       └── PredictionsTable.jsx # Full predictions table
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

### Backend Structure
```
api/
├── __init__.py
└── app.py                    # Flask server with all endpoints
```

## Configuration

### Backend (api/app.py)
- Port: 5000
- CORS: Enabled for all origins
- Supabase: Uses SupabaseManager from supabase_manager.py

### Frontend (dashboard/vite.config.js)
- Port: 3000
- Proxy: /api → http://localhost:5000

### Tailwind Theme (dashboard/tailwind.config.js)
```javascript
colors: {
  primary: '#3B82F6',    // Blue
  success: '#10B981',    // Green
  warning: '#F59E0B',    // Yellow
  danger: '#EF4444',     // Red
}
```

## Consensus Algorithm

```javascript
function calculateConsensus(prediction) {
  let agreements = 0
  
  // LiveSport: Win rate >= 60%
  if (prediction.livesport_win_rate >= 60) agreements++
  
  // Forebet: Prediction = '1' (home win)
  if (prediction.forebet_prediction === '1') agreements++
  
  // SofaScore: Home win prob > Away win prob
  if (prediction.sofascore_home_win_prob > prediction.sofascore_away_win_prob) 
    agreements++
  
  // Gemini: Recommendation = HIGH or LOCK
  if (prediction.gemini_recommendation === 'HIGH' || 
      prediction.gemini_recommendation === 'LOCK') 
    agreements++
  
  // Badge assignment
  if (agreements === 4) return '🔐 LOCK'
  if (agreements === 3) return '🟢 HIGH'
  if (agreements === 2) return '🟡 MEDIUM'
  return '❌ LOW'
}
```

## Real-Time Updates

Using React Query for automatic refetching:
```javascript
const { data } = useQuery({
  queryKey: ['predictions', days],
  queryFn: () => fetchRecentPredictions(days),
  refetchInterval: 60000  // Refetch every 60 seconds
})
```

## Deployment

### Option 1: Local Network
```bash
# Backend
python api/app.py  # Already binds to 0.0.0.0:5000

# Frontend (build)
cd dashboard
npm run build
# Serve dist/ with any static server
```

### Option 2: Cloud (Future)
- Backend: Deploy Flask to Heroku/Railway/Render
- Frontend: Deploy to Vercel/Netlify
- Database: Already on Supabase (cloud)

## Testing

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get recent predictions
curl http://localhost:5000/api/predictions/recent?days=7

# Get accuracy
curl http://localhost:5000/api/accuracy?days=30

# Get consensus picks
curl http://localhost:5000/api/consensus?min_agreement=3
```

### Test Frontend
```bash
cd dashboard
npm run dev
# Open http://localhost:3000 in browser
```

## Troubleshooting

### CORS Errors
- Ensure Flask CORS is enabled: `CORS(app)`
- Check Vite proxy configuration in vite.config.js

### API Connection Failed
- Verify Flask server is running on port 5000
- Check Supabase credentials in supabase_manager.py

### No Data Displayed
- Ensure Supabase database has predictions
- Run scraper to populate data:
  ```bash
  python livesport_h2h_scraper.py --mode auto --date 2025-11-18 --use-supabase
  ```

### React Query Errors
- Check browser console for API errors
- Verify API responses match expected format

## Future Enhancements

### Phase 7.1: Live Updates
- WebSocket connection for real-time data
- Push notifications for new predictions
- Live match score updates

### Phase 7.2: Advanced Analytics
- ROI tracking and profit/loss calculator
- Historical trend analysis
- Machine learning prediction confidence

### Phase 7.3: User Features
- User authentication
- Favorite picks/bookmarks
- Custom alerts and notifications
- Betting tracker integration

### Phase 7.4: Mobile App
- React Native mobile app
- Push notifications
- Offline mode with local storage

## Performance

### Backend Optimization
- Response caching (Redis)
- Database query optimization
- API rate limiting

### Frontend Optimization
- Code splitting
- Lazy loading components
- Memoization for expensive calculations
- Virtual scrolling for large tables

## Security

### Current
- Supabase Row Level Security enabled
- CORS configured for specific origins
- Environment variables for secrets

### Future
- JWT authentication
- API key for external access
- Rate limiting per user
- Input validation and sanitization

---

**Status:** ✅ Complete  
**Version:** 1.0.0  
**Last Updated:** November 18, 2025
