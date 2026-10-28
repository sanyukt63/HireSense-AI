# Scoring Guardrails

Candidate scoring should support recruiter review rather than replace it.

## Guardrails

- Keep scoring criteria tied to the job requirements.
- Preserve evidence behind important score components.
- Avoid using protected characteristics as ranking inputs.
- Flag uncertain or incomplete extraction results.
- Make model-version changes traceable.
- Allow recruiters to review the underlying candidate information.

## Score-explanation review

Before shipping a scoring change, review these points:
- Each displayed score has a stable, documented interpretation.
- Missing resume fields are treated as unknown, not automatically as negative evidence.
- The explanation references supported extracted information rather than invented details.
- Equivalent inputs produce consistent results for the same model and configuration.
- Model or weighting changes can be traced to a version or configuration update.

Use representative and edge-case examples during review; do not treat a score as the sole hiring decision.
