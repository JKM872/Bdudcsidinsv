# Sports Prediction Dashboard - Phase 7 Deployment

## Start Commands

### Development Mode

**Backend API:**
```bash
cd c:\Users\jakub\Desktop\BigOne
python api/app.py
```

**Frontend Dashboard:**
```bash
cd c:\Users\jakub\Desktop\BigOne\dashboard
npm run dev
```

Access: http://localhost:3000

---

## Production Build

### Build Frontend
```bash
cd c:\Users\jakub\Desktop\BigOne\dashboard
npm run build
```
Output: `dashboard/dist/`

### Serve Production Build
```bash
# Using Python HTTP server
cd dashboard/dist
python -m http.server 3000

# Or using npm serve
npm install -g serve
serve -s dist -l 3000
```

---

## Windows Batch Files

### `start_dashboard_dev.bat`
```batch
@echo off
echo Starting Sports Prediction Dashboard (Development)...

start cmd /k "cd /d c:\Users\jakub\Desktop\BigOne && echo Starting Backend API... && python api/app.py"
timeout /t 3
start cmd /k "cd /d c:\Users\jakub\Desktop\BigOne\dashboard && echo Starting Frontend... && npm run dev"

echo Dashboard starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
timeout /t 5
start http://localhost:3000
```

### `start_dashboard_prod.bat`
```batch
@echo off
echo Starting Sports Prediction Dashboard (Production)...

start cmd /k "cd /d c:\Users\jakub\Desktop\BigOne && echo Starting Backend API... && python api/app.py"
timeout /t 3
start cmd /k "cd /d c:\Users\jakub\Desktop\BigOne\dashboard\dist && echo Starting Frontend... && python -m http.server 3000"

echo Dashboard starting...
echo Access: http://localhost:3000
timeout /t 5
start http://localhost:3000
```

---

## Docker Deployment (Future)

### Dockerfile (Backend)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "api/app.py"]
```

### Dockerfile (Frontend)
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY dashboard/package*.json ./
RUN npm install
COPY dashboard/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

---

## Cloud Deployment

### Option 1: Vercel + Railway

**Frontend (Vercel):**
```bash
cd dashboard
npm install -g vercel
vercel
```

**Backend (Railway):**
1. Connect GitHub repo to Railway
2. Set root directory: `/`
3. Start command: `python api/app.py`
4. Add environment variables: SUPABASE_URL, SUPABASE_KEY

### Option 2: Netlify + Render

**Frontend (Netlify):**
```bash
cd dashboard
npm install -g netlify-cli
netlify deploy --prod
```

**Backend (Render):**
1. Create new Web Service
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn api.app:app`

---

## Monitoring

### Health Checks
```bash
# Backend
curl http://localhost:5000/api/health

# Frontend
curl http://localhost:3000
```

### Logs
```bash
# Backend logs (if using systemd)
journalctl -u dashboard-api -f

# Frontend logs
pm2 logs dashboard-frontend
```

---

## Backup Strategy

### Database (Supabase)
- Automatic daily backups (Supabase feature)
- Manual export: SQL dump from Supabase dashboard

### Code
- Git repository (already on GitHub)
- Regular commits and pushes

---

## Security Checklist

- [x] CORS configured for specific origins
- [x] Supabase RLS enabled
- [ ] API rate limiting (future)
- [ ] JWT authentication (future)
- [ ] HTTPS/SSL certificate (production)
- [ ] Environment variables for secrets
- [ ] Input validation
- [ ] SQL injection prevention (Supabase handles)

---

**Status:** Development Complete  
**Version:** 1.0.0  
**Date:** November 18, 2025
