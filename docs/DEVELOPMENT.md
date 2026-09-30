# Development Guide

HireSense AI is currently being built incrementally. The repository README is the source of truth for the current milestone and setup requirements.

## Local workflow

Create a virtual environment and install the pinned dependency ranges:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Copy the environment template before configuring local services:

```bash
cp .env.example .env
```

Apply migrations and start Django:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Safe development practices

- Keep `.env` out of version control.
- Never use real candidate documents or personally identifiable information for local testing.
- Use representative test fixtures instead.
- Keep AI scoring explainable and reproducible when implementing the scoring pipeline.
- Validate file uploads before passing documents to parsers.
