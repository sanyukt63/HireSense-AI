# 🤖 HireSense AI

> An AI-assisted resume screening and candidate shortlisting platform built with Django and PostgreSQL.

## 🎯 Project Goal

HireSense AI is being developed as a recruitment platform that can organize candidates, job postings, applications, resumes, assessments, and analytics in one system.

The project is currently in **Milestone 1 / architecture stage**. Product workflows and AI scoring are being developed incrementally.

## 🧩 Architecture

| App | Responsibility |
| --- | --- |
| `accounts` | Users, roles, candidate/recruiter profiles |
| `jobs` | Companies and job postings |
| `resume` | Resume uploads and structured candidate records |
| `recruitment` | Applications, review decisions, shortlists |
| `ai_engine` | Parsing, scoring, suggestions, model operations |
| `analytics` | Aggregate recruitment metrics |

The normalized data model is designed to keep candidate/job relationships queryable and AI assessments reproducible.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for application boundaries and the planned processing flow.

## 🛠️ Stack

- **Backend:** Django 5
- **Database:** PostgreSQL
- **Language:** Python
- **AI/NLP:** spaCy, Sentence Transformers, scikit-learn, and document-processing tools
- **Deployment direction:** Gunicorn + Render + managed PostgreSQL/object storage

## 🚀 Local Setup

### Prerequisites

- Python 3.10+
- PostgreSQL
- Git

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/sanyukt63/HireSense-AI.git
cd HireSense-AI
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables

The Django settings read these variables:

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Secret key used by Django |
| `DJANGO_DEBUG` | Set to `true` only for local development |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed host names |
| `DATABASE_URL` | PostgreSQL connection URL |

Example values for a local development session (replace the database username/password with your own):

```text
DJANGO_SECRET_KEY=replace-with-a-generated-secret
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/hiresense_db
```

Set these in your shell or a local environment file that is excluded from Git. Do not commit secrets or real candidate data.

### 4. Apply migrations and start the server

Create the PostgreSQL database first, then run:

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. Run checks and tests

```bash
python manage.py check
python manage.py test
```

## 🔍 AI Evaluation Principles

AI-assisted screening should remain explainable and reviewable. Candidate scores should be accompanied by the skills or evidence that contributed to the assessment, with recruiter decisions remaining subject to human review.

Use synthetic or anonymized candidate fixtures during development. Avoid exposing personal information in logs, test output, or sample data.

## 🗺️ Roadmap

- [ ] Candidate and recruiter authentication flows
- [ ] Job creation and application workflow
- [ ] Resume parsing pipeline
- [ ] Skill extraction and normalization
- [ ] Explainable candidate scoring
- [ ] Recruiter dashboard and analytics
- [ ] Automated tests
- [ ] Production deployment

## ⚠️ Development Status

This repository is under active development. Some workflows described in the architecture are planned rather than fully implemented.

## 🤝 Contributing

Issues, documentation improvements, testing, and implementation ideas are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for local development notes.

1. Fork the repository
2. Create a feature branch
3. Make a focused change
4. Test it
5. Open a pull request with a clear description

⭐ Star the project if you want to follow its development.
