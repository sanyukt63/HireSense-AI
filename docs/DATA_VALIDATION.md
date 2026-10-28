# Data Validation Principles

Candidate and recruitment data should be validated before it reaches business logic.

- Validate required fields at the API boundary.
- Normalize structured values consistently.
- Reject malformed identifiers and unsupported file types.
- Keep validation errors actionable.
- Avoid storing unnecessary sensitive information.
- Treat uploaded resume content as untrusted input.

Validation rules should be covered by automated tests as the application grows.

## Malformed-input checks

When handling candidate, job, or resume data, cover:
- Missing required fields and values containing only whitespace.
- Unexpected data types and malformed nested objects.
- Empty uploads and files that do not match the allowed format.
- Very large inputs and extraction results with no usable text.
- Safe error responses that do not expose stack traces or sensitive resume content.

Validate at the API boundary and add a regression test for each corrected failure mode.
