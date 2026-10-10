# Safe Test Data Policy

- Use synthetic candidate profiles in automated tests.
- Never commit real resumes, phone numbers, addresses, or credentials.
- Keep fixtures small and focused on a specific scenario.
- Include malformed and incomplete documents as synthetic edge cases.
- Review test output for accidental personal data before sharing logs.
- Keep test expectations independent of unstable external AI responses where possible.
