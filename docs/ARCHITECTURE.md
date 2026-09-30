# Architecture Notes

HireSense AI separates recruitment domain data from AI processing so that candidate and job records remain queryable independently of model operations.

## Application boundaries

- **accounts** — authentication, roles, and profiles
- **jobs** — companies and job postings
- **resume** — resume uploads and structured candidate records
- **recruitment** — applications, review decisions, and shortlists
- **ai_engine** — parsing, extraction, scoring, and model operations
- **analytics** — aggregate recruitment metrics

## Planned processing flow

```text
Resume upload
    |
    v
Document validation
    |
    v
Text extraction
    |
    v
Skill/entity normalization
    |
    v
Candidate representation
    |
    v
Explainable scoring
    |
    v
Recruiter review
```

The AI pipeline should remain auditable: store the inputs and model/version metadata needed to reproduce an assessment, while avoiding unnecessary storage of sensitive candidate information.

This document describes the intended architecture; implementation status can differ by milestone.
