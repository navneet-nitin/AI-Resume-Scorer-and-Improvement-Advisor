<div align="center">

<img src="https://raw.githubusercontent.com/navneet-nitin/AI-Resume-Scorer-and-Improvement-Advisor/main/Company%20Logo.jpeg" alt="CVDekho" width="150"/>

# CVDekho

### Know Your Resume Score in Seconds 🎯

[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)

<br/>

**Upload your resume → Get an AI-powered score across 10 parameters → See exactly what to fix → Land more interviews.**

<br/>

[🌐 Try CVDekho Live](#) &nbsp;&nbsp;|&nbsp;&nbsp; [📖 API Docs](#api-reference) &nbsp;&nbsp;|&nbsp;&nbsp; [🐛 Report a Bug](https://github.com/navneet-nitin/AI-Resume-Scorer-and-Improvement-Advisor/issues)

<br/>

> 🚧 **Frontend coming soon.** Backend is fully deployed and live.

</div>

---

## What Is CVDekho? 🤔

Most resumes never reach a human recruiter — they get filtered out by ATS software first. CVDekho solves this by giving students and job seekers the same lens a recruiter uses: honest, specific, AI-powered feedback in seconds.

Upload a PDF → our backend extracts the text, sends it through a carefully engineered prompt to **Google Gemini 2.5 Flash**, and returns a **0–100 score** broken down across 10 weighted parameters — complete with your top 3 critical issues, missing ATS keywords, and AI-rewritten sections.

No login. No fluff. Just honest feedback.

---

## How It Works 🔄

```
You upload a PDF resume
         │
         ▼
   ┌─────────────────────────────────┐
   │        FastAPI Backend          │
   │                                 │
   │  1. Validate PDF                │
   │     (type, size, content check) │
   │                                 │
   │  2. Upload → Supabase Storage   │
   │                                 │
   │  3. Extract text → PyMuPDF      │
   │                                 │
   │  4. Build structured prompt     │
   │                                 │
   │  5. Call Gemini 2.5 Flash       │
   │                                 │
   │  6. Parse + validate JSON       │
   │                                 │
   │  7. Save result → Supabase DB   │
   └─────────────────────────────────┘
         │
         ▼
   Score + Feedback + Rewrites
   returned in ~10–15 seconds
```

---

## Features ✨

- 📄 **PDF Upload** — validated client-side and server-side (type, size, content)
- 🤖 **AI Scoring** — Gemini 2.5 Flash evaluates across 10 weighted parameters
- 📊 **Detailed Breakdown** — per-parameter score, weight, feedback, and status badge
- 🚨 **Top 3 Critical Issues** — the most impactful problems to fix, ranked
- 🔑 **ATS Keyword Gaps** — missing industry keywords identified for your target role
- ✍️ **AI Rewrites** — your professional summary and weakest bullet, rewritten
- 💾 **Persistent Results** — retrieve your scan anytime via submission ID
- ⚡ **Fast** — ~10–15s response using Gemini Flash

---

## Tech Stack 🛠️

| Layer | Technology | Why |
|---|---|---|
| **Backend Framework** | FastAPI 0.135 | Async, built-in validation, auto Swagger docs |
| **AI Model** | Google Gemini 2.5 Flash | Free tier, fast, structured JSON output |
| **PDF Parsing** | PyMuPDF 1.27 | Most accurate text extraction, handles complex layouts |
| **Database** | Supabase PostgreSQL | Free tier, structured data, REST API + Python client |
| **File Storage** | Supabase Storage | Private bucket — no public access to uploaded files |
| **Backend Hosting** | Render.com | Free tier, zero DevOps, FastAPI native |
| **Frontend Hosting** | Vercel *(coming soon)* | Instant deploys, optimised for static sites |

---

## Project Structure 📁

```
AI-Resume-Scorer/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes.py              # POST /api/analyze-resume
│   │   │   └── health.py              # GET /health
│   │   ├── services/
│   │   │   ├── gemini_service.py      # Gemini API + JSON validation + retry logic
│   │   │   ├── pdf_service.py         # PyMuPDF text extraction pipeline
│   │   │   └── supabase_service.py    # DB inserts, PDF uploads, result updates
│   │   ├── utils/
│   │   │   ├── prompt_builder.py      # 10-parameter structured Gemini prompt
│   │   │   └── validators.py          # PDF type / size / content validation
│   │   ├── config.py                  # Environment variables + constants
│   │   └── main.py                    # FastAPI app, CORS, router registration
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                          # 🚧 Coming soon
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## API Reference 📡

Base URL: `https://your-app.onrender.com` *(update once deployed)*

Interactive docs available at `/docs` (Swagger UI) or `/redoc` on the live URL.

---

### `POST /api/analyze-resume`

Runs the full AI analysis pipeline on a resume PDF.

**Request** — `multipart/form-data`

| Field | Type | Required | Notes |
|---|---|---|---|
| `file` | File | ✅ | PDF only, max 5 MB |
| `user_email` | string | ❌ | Optional, stored for result retrieval |

**Response `200 OK`**

```json
{
  "submission_id": "3f2a1c...",
  "overall_score": 62,
  "grade": "C",
  "overall_verdict": "This resume has a solid skills section but lacks quantified achievements...",
  "parameters": [
    {
      "name": "Projects & Experience",
      "score": 5,
      "weight": 20,
      "feedback": "Bullet points describe tasks, not outcomes. No metrics present.",
      "status": "improve"
    }
  ],
  "top_3_critical_issues": [
    "No quantified achievements across any bullet point",
    "Professional summary is generic and role-agnostic",
    "Missing core ATS keywords for software engineering roles"
  ],
  "ats_keywords_missing": ["REST API", "CI/CD", "Docker", "Agile", "System Design"],
  "rewritten_sections": {
    "summary": "Final-year ECE student at HIT with hands-on experience in...",
    "one_weak_bullet_rewrite": "ORIGINAL: Worked on ML model | REWRITTEN: Built a Random Forest classifier achieving 87% accuracy on 10K+ records, cutting manual review time by 40%"
  }
}
```

**Error Codes**

| Status | Meaning |
|---|---|
| `400` | Invalid file type, image uploaded, file too large, or empty file |
| `422` | Scanned/image-only PDF — no extractable text |
| `500` | Gemini API error or database write failed |

---

### `GET /api/result/{submission_id}`

Retrieve a previously analysed result by UUID.

`200` — same structure as POST response &nbsp;·&nbsp; `404` — submission not found

---

### `GET /health`

```json
{ "status": "ok", "service": "resume-scorer-api" }
```

---

## Scoring System 🎯

Gemini evaluates every resume through the lens of a senior technical recruiter. Here's exactly how the score is calculated:

| # | Parameter | Weight | What's Evaluated |
|---|---|---|---|
| 1 | Contact Information | 5% | Name, email, phone, LinkedIn, GitHub — flags unprofessional emails |
| 2 | Professional Summary | 10% | Existence, specificity, role target — penalises generic boilerplate |
| 3 | Skills Section | 10% | Categorisation, realism, context — detects padding |
| 4 | **Projects & Experience** | **20%** | Action verbs, quantified achievements, impact statements |
| 5 | ATS Keywords | 15% | Industry-standard keywords — identifies up to 6 missing |
| 6 | Education | 5% | CGPA, graduation year, relevant coursework |
| 7 | Formatting & Clarity | 10% | 6-second scanability, consistent structure |
| 8 | Resume Length | 5% | Fresher: 1 page ideal. Penalises under 300 words or over 2 pages |
| 9 | Achievements vs Responsibilities | 10% | Target: 60%+ achievement-oriented bullets |
| 10 | Overall Impression | 10% | Grammar, tense, polish — would a recruiter shortlist this? |

**Grading Scale:**

| Grade | Score | What It Means |
|---|---|---|
| 🟢 **A** | 85–100 | Recruiter will very likely shortlist |
| 🔵 **B** | 70–84 | Strong candidate, minor gaps |
| 🟡 **C** | 55–69 | Will be filtered by ATS or HR |
| 🟠 **D** | 40–54 | Significant rework needed |
| 🔴 **F** | 0–39 | Complete restructure required |

> 📌 Most student resumes score **35–55**. The AI is calibrated to be honest, not encouraging. 70+ means genuinely well-written.

---

## Database Schema 🗄️

**Table: `resume_submissions`**

```sql
CREATE TABLE resume_submissions (
  id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at             TIMESTAMPTZ DEFAULT now(),
  user_email             TEXT,
  file_url               TEXT NOT NULL,
  extracted_text_preview TEXT,
  overall_score          INTEGER,
  grade                  TEXT,
  full_result_json       JSONB,
  gemini_model_used      TEXT DEFAULT 'gemini-2.5-flash',
  processing_time_ms     INTEGER
);
```

Also create a **private** Supabase Storage bucket named `resumes`.

---

## Privacy & Data Handling 🔒

We believe in being transparent. Here's exactly what happens to your resume:

| What | Details |
|---|---|
| **What is stored** | Your PDF file and the extracted text, along with the AI-generated score and feedback |
| **Where it is stored** | Supabase (PostgreSQL database + private storage bucket) — files are not publicly accessible |
| **Who can access it** | Only the CVDekho backend service via a private API key — no human manually reviews your CV |
| **Why we store it** | So you can retrieve your result anytime using your submission ID |
| **How long we keep it** | MVP: indefinitely (deletion on request) — future versions will add auto-expiry |
| **Do we share it** | No. Your CV data is never sold, shared, or used to train any model |

> ⚠️ **For users:** By uploading your resume, you acknowledge that it will be stored as described above. If you'd like your data deleted, open an [issue](https://github.com/navneet-nitin/AI-Resume-Scorer-and-Improvement-Advisor/issues) with your submission ID.

> 💡 **For developers:** Under India's **Digital Personal Data Protection Act 2023 (DPDPA)**, storing personal data requires informed user consent and a clear purpose. This section serves as the disclosure. Add a visible consent line on your upload form before going live: *"Your CV is stored securely and used only to generate your score."*

---

## Environment Variables 🔐

Create a `.env` file inside `backend/` — **never commit this file.**

```env
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
SUPABASE_BUCKET_NAME=resumes
```

Get your free Gemini API key at [aistudio.google.com](https://aistudio.google.com/app/apikey) — no credit card needed.

---

<details>
<summary>🧑‍💻 <strong>Local Development Setup</strong> (for contributors)</summary>

<br/>

> The live app is hosted — you only need this if you're contributing to the codebase.

```bash
# 1. Clone the repo
git clone https://github.com/navneet-nitin/AI-Resume-Scorer-and-Improvement-Advisor.git
cd AI-Resume-Scorer-and-Improvement-Advisor/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your .env file (see Environment Variables above)

# 5. Start the server
uvicorn app.main:app --reload --port 8000
```

API runs at `http://localhost:8000` &nbsp;·&nbsp; Swagger UI at `http://localhost:8000/docs`

</details>

---

## Contributing 🤝

We use Git Flow. Please follow this workflow:

```bash
# Create a feature branch from develop
git checkout -b feature/your-feature-name

# Commit using conventional commits
git commit -m "feat: add job description matching"

# Push and open a PR targeting → develop (not main)
git push origin feature/your-feature-name
```

| Prefix | When to use |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `refactor:` | Code cleanup, no behaviour change |
| `docs:` | Documentation only |

**Rules:** minimum 1 peer review before merge · no direct commits to `main` · no API keys in code.

---

## Team 👥

Built by **Group 37** — HIT AI Systems & Industry Readiness Programme 2026 🎓

| Contributor | Role |
|---|---|
| [Navneet Nitin](https://github.com/navneet-nitin) | 🧠 Product Lead · Prompt Engineer · Backend · Gemini Integration |
| Nitin | ⚙️ Tech Lead · Frontend · End-to-End Integration |
| Ishit | 🔧 Backend Lead · FastAPI Architecture |
| Khushi | 📄 PDF Extraction · PyMuPDF Pipeline |
| Neha | 🗄️ Database · Supabase Schema & Storage |
| Nishant | 🎨 Frontend Developer |
| Mayank | 📊 Result Page UI · Score Visualisation |
| Manish | 🖥️ UI Components · Result Page |
| Nabanita | 🎤 Demo Lead · Pitch |
| Juthika | 🎤 Demo Support · Presentation |

---

## License 📄

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for full terms.

Copyright © 2026 Navneet Nitin & Group 37, Haldia Institute of Technology.

---

<div align="center">

Made with ❤️ at **Haldia Institute of Technology**

*HIT AI Systems & Industry Readiness Programme 2026*

**[⬆ Back to top](#cvdekho)**

</div>
