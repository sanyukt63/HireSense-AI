# HireSense AI

AI-powered resume screening and candidate shortlisting platform built with Django and PostgreSQL.

## Milestone 1 status

The project scaffold, PostgreSQL-ready settings, custom user model, static/media configuration, app boundaries, and initial architecture are in place. Product workflows are intentionally deferred to later milestones.

## Applications

| App | Responsibility |
| --- | --- |
| `accounts` | Identity, roles, candidate/recruiter profiles |
| `jobs` | Company and job postings |
| `resume` | Resume uploads and structured candidate records |
| `recruitment` | Applications, review decisions, shortlists |
| `ai_engine` | Parsing, scoring, suggestions and model operations |
| `analytics` | Aggregate dashboard metrics |

## Planned normalized data model

`User` is the authentication identity and holds a product role. `CandidateProfile` and `RecruiterProfile` each extend one user. A `RecruiterProfile` belongs to a `Company`; a `Company` has many `Job` records. A `CandidateProfile` owns many versioned `Resume` records. `Application` is the unique candidate/job join and has an optional selected resume. `ApplicationAssessment` belongs to one application and stores reproducible ATS component scores and a parser/model version. `Skill` is canonical; `ResumeSkill` and `JobSkillRequirement` are many-to-many join tables with proficiency/importance metadata. Education, employment, projects, and certifications belong to a resume rather than being serialized into one unqueryable field.

This prevents duplicated user/company/skill data, allows candidate resubmission, and keeps historical AI scores auditable.

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set a secure key and PostgreSQL `DATABASE_URL`.
4. Create database `hiresense_db` and its role in PostgreSQL.
5. Run `python manage.py makemigrations` then `python manage.py migrate`.
6. Run `python manage.py runserver`.

## Environment

`DATABASE_URL` uses PostgreSQL form: `postgresql://USER:PASSWORD@HOST:5432/DBNAME`.

## Deployment direction

Render will use Gunicorn, `collectstatic`, an environment-provided `DATABASE_URL`, and `DJANGO_DEBUG=False`. Persist uploaded files in object storage before production release; Render's local filesystem is not durable.
