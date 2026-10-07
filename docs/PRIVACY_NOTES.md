# Candidate Privacy Notes

Resume and recruitment data can contain sensitive personal information.

## Development rules

- Never commit real candidate resumes or personal data.
- Keep secrets and database credentials outside source control.
- Use synthetic or anonymized data for tests.
- Restrict access to uploaded documents.
- Avoid logging raw resume contents unnecessarily.
- Remove temporary files after processing when they are no longer required.

Any production deployment should apply appropriate access controls, retention policies, and applicable privacy requirements.
