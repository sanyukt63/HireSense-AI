# API Guidelines

HireSense AI APIs should keep recruitment workflows predictable and auditable.

## Response conventions

- Return clear HTTP status codes.
- Use consistent JSON field names.
- Validate user-controlled input at the API boundary.
- Never expose secrets or internal stack traces.
- Return stable identifiers for resources.

## AI evaluation

AI-generated scores or recommendations should include enough evidence for a recruiter to understand the result. Human review remains part of the decision flow.

## Changes

API changes should include updated documentation and tests where practical. Breaking changes should be called out explicitly in the pull request.
