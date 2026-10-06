# Data Validation Principles

Candidate and recruitment data should be validated before it reaches business logic.

- Validate required fields at the API boundary.
- Normalize structured values consistently.
- Reject malformed identifiers and unsupported file types.
- Keep validation errors actionable.
- Avoid storing unnecessary sensitive information.
- Treat uploaded resume content as untrusted input.

Validation rules should be covered by automated tests as the application grows.
