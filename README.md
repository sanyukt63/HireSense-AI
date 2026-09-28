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

## 🛠️ Stack

- **Backend:** Django
- **Database:** PostgreSQL
- **Language:** Python
- **AI layer:** planned parsing/scoring pipeline
- **Deployment direction:** Gunicorn + Render + managed PostgreSQL/object storage

## 🚀 Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the environment template:

```bash
cp .env.example .env
```

4. Configure a secure Django key and PostgreSQL `DATABASE_URL`.
5. Create the `hiresense_db` database and PostgreSQL role.
6. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Start Django:

```bash
python manage.py runserver
```

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

1. Fork the repository
2. Create a feature branch
3. Make a focused change
4. Test it
5. Open a pull request with a clear description

⭐ Star the project if you want to follow its development.
