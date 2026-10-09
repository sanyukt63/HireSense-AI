# Resume Upload Security Checks

- Enforce an allowlist of supported document types.
- Apply a reasonable upload size limit.
- Do not trust the filename or client-provided MIME type alone.
- Store uploads outside executable application paths.
- Use generated storage names rather than raw user filenames.
- Keep access to uploaded resumes restricted.
- Return safe errors and avoid logging document contents.
