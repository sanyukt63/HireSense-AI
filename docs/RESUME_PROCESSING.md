# Resume Processing Flow

A predictable processing pipeline helps keep resume analysis reproducible.

1. Receive the uploaded document.
2. Validate file type and size.
3. Extract text safely.
4. Normalize relevant fields.
5. Run skill or job matching analysis.
6. Store structured results and provenance.
7. Present evidence for recruiter review.

Failures at any stage should produce a clear status instead of silently producing incomplete results.
