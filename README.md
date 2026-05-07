# Aperture MVP

A full-stack social feed prototype where users control the recommendation algorithm.

## Stack

- React + Vite frontend
- Python FastAPI backend
- SQLite database

## Local setup

### Backend

```bash
cd server
python -m venv .venv
source .venv/bin/activate # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd client
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173`.

## Deploy

### Backend on Render

Create a new Web Service from this repo.

- Root Directory: `server`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `CORS_ORIGINS=https://your-vercel-domain.vercel.app`

For MVP SQLite works, but Render free instances may reset disk state. For durable production data, swap SQLite for Postgres.

### Frontend on Vercel

- Root Directory: `client`
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment variable: `VITE_API_URL=https://your-render-service.onrender.com`

## MVP behavior

Move the algorithm sliders and the frontend calls `/api/feed/rank`. The backend reorders posts based on metadata scores and returns explanations for why each post appears.
