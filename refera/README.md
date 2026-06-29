# Refera — AI Job Referral Network

Production-ready SaaS platform connecting job seekers with employee referrers, powered by AI resume analysis, job matching, and referral message generation.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React, Tailwind CSS, Framer Motion |
| Backend | FastAPI, SQLAlchemy, JWT Auth |
| Database | PostgreSQL |
| Payments | Razorpay (demo mode without keys) |
| Storage | Local / AWS S3 |
| AI | OpenAI (optional — smart fallbacks included) |
| Deploy | Vercel (frontend) + Render (backend) |

## Project Structure

```
refera/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLAlchemy
│   │   ├── models/              # DB models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API routes
│   │   ├── services/            # Business logic
│   │   └── auth/                # JWT security
│   ├── seed.py                  # Demo data
│   ├── requirements.txt
│   ├── render.yaml              # Render deploy config
│   └── Procfile
└── frontend/
    ├── src/
    │   ├── app/                 # Next.js pages
    │   ├── components/          # UI components
    │   └── lib/                 # API client & auth
    └── vercel.json
```

## Features

- **Landing Page** — Hero, problem statement, how it works, features, pricing, testimonials, FAQ
- **User Dashboard** — Resume upload, ATS score, job matches, referral tracking
- **Resume Analyzer** — PDF/DOCX parsing, keyword analysis, ATS scoring, AI feedback
- **Job Matching** — Skill-based eligibility scoring
- **Referral System** — Pending/Accepted/Rejected status, referral limits
- **AI Features** — Referral messages, interview questions, eligibility chatbot
- **Admin Panel** — Users, jobs, referrals, analytics
- **Payments** — Razorpay free/premium plans

## Quick Start (Local)

### 1. Backend

```bash
cd refera/backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DATABASE_URL (PostgreSQL required)

# Start PostgreSQL locally, then:
python seed.py
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd refera/frontend
cp .env.example .env.local
npm install
npm run dev
```

App: http://localhost:3000

## Demo Accounts

After running `python seed.py`:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@refera.app | Demo@12345 |
| Candidate | demo@refera.app | Demo@12345 |
| Premium | emma.wilson@refera.app | Demo@12345 |
| Employee | sarah.chen@refera.app | Demo@12345 |

## Deploy to Render (Backend)

1. Push repo to GitHub
2. Create a **PostgreSQL** database on Render
3. Create a **Web Service** pointing to `refera/backend`
4. Set environment variables:
   - `DATABASE_URL` — from Render PostgreSQL
   - `SECRET_KEY` — generate a random string
   - `FRONTEND_URL` — your Vercel URL
   - `OPENAI_API_KEY` (optional)
   - `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` (optional)
   - `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` (optional)
5. Build command: `pip install -r requirements.txt && python seed.py`
6. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Or use the included `render.yaml` Blueprint.

## Deploy to Vercel (Frontend)

1. Import the repo on [vercel.com](https://vercel.com)
2. Set **Root Directory** to `refera/frontend`
3. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://your-api.onrender.com/api/v1`
   - `NEXT_PUBLIC_GOOGLE_CLIENT_ID` (optional)
4. Deploy

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/google` | Google OAuth |
| POST | `/api/v1/resumes/upload` | Upload resume |
| POST | `/api/v1/resumes/{id}/analyze` | ATS analysis |
| GET | `/api/v1/jobs/` | List jobs |
| POST | `/api/v1/jobs/match` | Match jobs |
| POST | `/api/v1/referrals/` | Create referral |
| POST | `/api/v1/ai/eligibility` | AI eligibility check |
| POST | `/api/v1/ai/referral-message` | AI message generator |
| GET | `/api/v1/admin/stats` | Admin analytics |

## Pages

| Page | Route |
|------|-------|
| Home | `/` |
| Login | `/login` |
| Signup | `/signup` |
| Pricing | `/pricing` |
| Dashboard | `/dashboard` |
| Resume Analyzer | `/dashboard/resume` |
| Job Matches | `/dashboard/jobs` |
| Referrals | `/dashboard/referrals` |
| Profile | `/dashboard/profile` |
| Admin | `/dashboard/admin` |

## License

MIT
