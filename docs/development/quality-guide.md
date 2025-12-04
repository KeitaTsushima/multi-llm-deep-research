# Quality Guide

This document defines the **minimum quality bar** for code that can be merged into the main branch.

The goal is to keep the rules **lightweight but explicit**, so humans, CodeRabbit, and AI tools can all align on what "good enough" means.

---

## 1. Scope

These rules apply to all production code in the project.

Adjust this section based on your tech stack (e.g., Node.js + TypeScript, Python, Go, etc.).

---

## 2. General Coding Rules

1. **Type safety**
   - Use strict type checking where available (TypeScript `strict: true`, mypy strict mode, etc.).
   - Avoid `any` / dynamic types. If you must use them, add a comment explaining why.

2. **Explicit error handling**
   - Do not silently swallow errors.
   - If an operation fails, the error must be:
     - propagated as an exception, or
     - converted into a clear error result for the caller.

3. **No noisy debug logs in main**
   - Logging is acceptable, but avoid excessive debug noise in merged code.
   - Prefer short, actionable messages ("Failed to process item X" etc.).

4. **Small, focused modules**
   - Separate concerns:
     - Entry points (CLI, API handlers) separate from business logic
     - Business logic in dedicated service/domain modules
     - Models and types in their own files
   - Avoid mixing different layers of responsibility.

5. **No PII in logs**
   - Never log Personally Identifiable Information (emails, passwords, tokens, etc.).
   - Mask or redact sensitive data before logging.

---

## 3. Error Handling Standards

1. **Use standard error vocabulary**
   - ValidationError: Invalid input
   - NotFoundError: Resource not found
   - UnauthorizedError: Authentication failed
   - ForbiddenError: Authorization failed
   - ServiceUnavailableError: External service unavailable
   - TimeoutError: Operation timed out

2. **Timeout and cancellation**
   - Use AbortController/cancellation tokens for long-running operations
   - Set reasonable timeout values
   - Propagate cancellation to dependent operations

---

## 4. Tests & CI

- All code must compile/build (`npm run build`, `make build`, etc.).
- All defined tests must pass (`npm test`, `pytest`, etc.).
- For early versions, prioritize:
  - Working code with a few reliable smoke tests
  - Over high coverage percentages.

See `docs/development/testing-guide.md` for more details on the testing approach.

---

## 5. PR Expectations (for humans & AI tools)

For each PR:

- Code **compiles** and **passes existing tests**.
- New or changed behavior is briefly documented (in code comments and/or docs).
- Breaking changes are clearly described in the PR description.
- Security considerations are noted if applicable.

---

## 6. Security Basics

- **Input validation**: Validate all external input
- **SQL injection**: Use parameterized queries
- **XSS**: Sanitize user-generated content in web UIs
- **Authentication**: Never store passwords in plaintext
- **Dependencies**: Keep dependencies up to date
