# API Conventions

API endpoints should use predictable request and response structures.

## Conventions

- Use nouns for resource-oriented paths.
- Validate request payloads at the API boundary.
- Return meaningful HTTP status codes.
- Keep error responses structured and consistent.
- Never expose stack traces in production responses.
- Document authentication requirements for protected endpoints.
- Keep pagination and filtering behavior consistent across list endpoints.

When an endpoint changes, update its documentation and tests in the same change.
