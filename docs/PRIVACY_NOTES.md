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

## Privacy review for test fixtures

Before adding fixtures or debugging output, check that:
- Tests use synthetic candidate and resume data wherever possible.
- Logs omit resume text, contact details, access tokens, and other unnecessary personal data.
- Uploaded files are stored only for the required duration and access scope.
- Error messages do not echo untrusted file content.
- Any sample data added to the repository is clearly fictional.

Review these safeguards whenever upload, extraction, or logging behavior changes.
