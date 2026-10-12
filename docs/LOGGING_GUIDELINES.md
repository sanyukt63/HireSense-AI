# Privacy-Aware Logging Guidelines

Application logs should help diagnose failures without exposing sensitive candidate information.

- Prefer request IDs and structured status fields.
- Do not log raw resume text or authentication secrets.
- Sanitize user-controlled values before logging.
- Keep production log access restricted.
- Define retention appropriate to operational needs.
- Include enough context to trace failures without copying entire payloads.
