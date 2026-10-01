"""Parsing and scoring services with no view or request dependencies."""
import re
from functools import lru_cache
from pathlib import Path

from django.db import transaction

from .models import ATSAssessment, JobSkillRequirement, ResumeParseResult, ResumeSkill, Skill

DEFAULT_SKILLS = (
    "Python", "Django", "JavaScript", "React", "HTML", "CSS", "SQL", "PostgreSQL",
    "Docker", "AWS", "Git", "REST", "Java", "C++", "Machine Learning", "Pandas",
    "scikit-learn", "spaCy", "Bootstrap", "Linux", "Kubernetes", "Azure",
)
SKILL_ALIASES = {
    "reactjs": "React",
    "react.js": "React",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "scikit learn": "scikit-learn",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "rest api": "REST",
    "rest apis": "REST",
}
PARSER_VERSION = "rule-based-v2"
SCORING_VERSION = "ats-v2"


def build_resume_suggestions(extracted_data):
    """Generate actionable resume improvement suggestions from parsed resume data."""
    skills = {str(value).lower() for value in extracted_data.get("skills", [])}
    missing_skills = [
        skill for skill in ("Python", "Django", "SQL", "Docker", "AWS", "React", "JavaScript")
        if skill.lower() not in skills
    ]
    better_keywords = [
        keyword for keyword in ("Python", "Django", "PostgreSQL", "REST APIs", "Cloud", "Machine Learning")
        if keyword.lower() not in skills
    ]
    return {
        "missing_skills": missing_skills,
        "better_keywords": better_keywords,
        "formatting_tips": [
            "Add a concise summary section near the top.",
            "Use consistent section headings and bullet points.",
            "Quantify achievements with metrics and outcomes.",
        ],
        "suggested_certifications": [
            "AWS Certified Cloud Practitioner",
            "Google Data Analytics",
            "Certified Kubernetes Administrator",
        ],
        "suggested_projects": [
            "Build a production-ready Django API with authentication and testing.",
            "Create a polished analytics dashboard with PostgreSQL and dashboards.",
        ],
    }


def extract_document_text(resume):
    extension = Path(resume.original_filename).suffix.lower()
    with resume.document.open("rb") as source:
        if extension == ".pdf":
            import fitz
            document = fitz.open(stream=source.read(), filetype="pdf")
            try:
                return "\n".join(page.get_text() for page in document)
            finally:
                document.close()
        if extension == ".docx":
            from docx import Document
            return "\n".join(paragraph.text for paragraph in Document(source).paragraphs)
    raise ValueError("Unsupported resume format. Upload a PDF or DOCX file.")


def _normalize_skill_name(name):
    key = re.sub(r"\s+", " ", name.strip().lower())
    return SKILL_ALIASES.get(key, name.strip())


def _canonical_skills():
    existing = list(Skill.objects.values_list("name", flat=True))
    return tuple(dict.fromkeys((*DEFAULT_SKILLS, *existing, *SKILL_ALIASES.values())))


def _matched_skills(text):
    normalized = text.lower()
    matches = []
    for skill in _canonical_skills():
        aliases = [skill]
        aliases.extend(alias for alias, canonical in SKILL_ALIASES.items() if canonical.lower() == skill.lower())
        if any(re.search(r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)", normalized) for alias in aliases):
            matches.append(_normalize_skill_name(skill))
    return sorted(set(matches), key=str.lower)


def _experience_years(text):
    values = [float(value) for value in re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)", text.lower())]
    return max(values, default=0.0)


def _education_mentions(text):
    lowered = text.lower()
    return [
        term for term in ("phd", "master", "bachelor", "b.tech", "b.e.", "mba", "diploma")
        if term in lowered
    ]


@transaction.atomic
def parse_resume(resume):
    text = extract_document_text(resume).strip()
    if not text:
        raise ValueError("The uploaded resume does not contain extractable text.")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone_match = re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", text)
    skills = _matched_skills(text)
    data = {
        "name": lines[0] if lines else "",
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "skills": skills,
        "experience_years": _experience_years(text),
        "education": _education_mentions(text),
        "projects": [line for line in lines if "project" in line.lower()][:10],
        "certifications": [line for line in lines if "certif" in line.lower()][:10],
    }
    result, _ = ResumeParseResult.objects.update_or_create(
        resume=resume,
        defaults={"raw_text": text, "extracted_data": data, "parser_version": PARSER_VERSION},
    )
    ResumeSkill.objects.filter(resume=resume).delete()
    for name in skills:
        skill, _ = Skill.objects.get_or_create(
            normalized_name=name.lower(),
            defaults={"name": name},
        )
        ResumeSkill.objects.create(resume=resume, skill=skill)
    return result


def parse_job_requirements(job):
    skills = _matched_skills(job.description)
    JobSkillRequirement.objects.filter(job=job).delete()
    for name in skills:
        skill, _ = Skill.objects.get_or_create(
            normalized_name=name.lower(),
            defaults={"name": name},
        )
        JobSkillRequirement.objects.create(job=job, skill=skill)
    return skills


@lru_cache(maxsize=1)
def _get_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def _semantic_similarity(first, second):
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        model = _get_embedding_model()
        embeddings = model.encode([first, second])
        return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    except Exception:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform([first, second])
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def _keyword_similarity(first, second):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    matrix = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=3000,
    ).fit_transform([first, second])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


@transaction.atomic
def score_application(application):
    if not application.resume:
        raise ValueError("This application no longer has a resume to score.")

    parsed = parse_resume(application.resume)
    required_names = parse_job_requirements(application.job)
    candidate_skills = {str(value) for value in parsed.extracted_data.get("skills", [])}
    required_skills = set(required_names)
    matched_skills = sorted(candidate_skills & required_skills, key=str.lower)
    skill_score = 100 * len(matched_skills) / len(required_skills) if required_skills else 0

    candidate_experience = float(parsed.extracted_data.get("experience_years", 0))
    required_experience = float(application.job.minimum_experience_years)
    experience_score = (
        100 if required_experience == 0
        else min(100, 100 * candidate_experience / required_experience)
    )

    education_score = 100 if not application.job.education_requirement else (
        100 if parsed.extracted_data.get("education") else 0
    )

    keyword_score = _keyword_similarity(parsed.raw_text, application.job.description) * 100
    semantic_score = max(0, min(100, _semantic_similarity(parsed.raw_text, application.job.description) * 100))
    final_score = (
        skill_score * 0.35
        + experience_score * 0.15
        + education_score * 0.10
        + keyword_score * 0.20
        + semantic_score * 0.20
    )

    details = {
        "matched_skills": matched_skills,
        "missing_skills": sorted(required_skills - candidate_skills, key=str.lower),
        "candidate_experience_years": candidate_experience,
        "required_experience_years": required_experience,
        "scoring_components": {
            "skills_weight": 0.35,
            "experience_weight": 0.15,
            "education_weight": 0.10,
            "keyword_weight": 0.20,
            "semantic_weight": 0.20,
        },
    }
    assessment, _ = ATSAssessment.objects.update_or_create(
        application=application,
        defaults={
            "skill_score": skill_score,
            "experience_score": experience_score,
            "education_score": education_score,
            "keyword_score": keyword_score,
            "semantic_score": semantic_score,
            "final_score": final_score,
            "score_details": details,
            "scoring_version": SCORING_VERSION,
        },
    )
    return assessment
