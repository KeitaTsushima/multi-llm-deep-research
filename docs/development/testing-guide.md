# Testing Guide

This document provides a lightweight testing strategy for early-stage projects.

The strategy is intentionally minimal but focuses on the **most fragile areas** of your application.

---

## 1. Test Pyramid

For early versions, focus on two levels:

1. **Unit tests**
   - Pure logic and transformations (no external dependencies).
   - Business logic, calculations, data transformations.
   - Helper/utility functions.

2. **Integration / smoke tests**
   - Small end-to-end flows that:
     - Exercise critical paths through your application.
     - Verify that key outputs are produced correctly.

No formal E2E UI tests are required in early versions (unless you have a GUI).

---

## 2. What to Test

### 2.1 Unit Tests

**Test these:**
- **Public methods**: Functions exposed in your API
- **Business logic**: Calculations, validations, transformations
- **Error handling**: Edge cases and error conditions

**Don't test:**
- Private methods (test them through public APIs)
- Trivial getters/setters
- External library code

**Example test cases:**
- Happy path (normal input)
- Edge cases (empty, null, boundary values)
- Error handling (invalid input, failures)

### 2.2 Integration / Smoke Tests

Test critical workflows end-to-end:

1. Use realistic but minimal test data
2. Verify expected outputs are created
3. Check that errors are properly surfaced

**Error handling tests:**
- Missing/invalid input: Expect non-zero exit code or exception
- External service failures: Verify graceful degradation
- These tests should be minimal but confirm failures are detected

---

## 3. Test Doubles (Mock, Stub, Fake)

Use appropriate test doubles for external dependencies:

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Stub** | Return fixed values | Configuration, simple responses |
| **Mock** | Verify calls/behavior | API calls, verify interactions |
| **Fake** | Lightweight implementation | In-memory DB, filesystem |

---

## 4. Running Tests

- All tests should run via a single command:
  - `npm test`, `pytest`, `go test`, etc.

- CI should at minimum:
  - Install dependencies
  - Build the project
  - Run all tests

---

## 5. Test File Organization

**Option 1: Co-located (recommended for small projects)**
```
src/
  services/
    user-service.ts
    user-service.test.ts
```

**Option 2: Separate test directory**
```
src/
  services/
    user-service.ts
tests/
  unit/
    services/
      user-service.test.ts
```

---

## 6. Future Extensions

As your project grows, consider adding:

- **Contract tests**: For API boundaries and microservices
- **Performance tests**: For critical paths
- **Property-based tests**: For pure functions
- **Snapshot tests**: For complex data structures

For early versions, the priority is:

- Avoiding regressions in critical paths
- Ensuring core logic behaves predictably
- Fast feedback loop (tests should run quickly)

---

## References

For more comprehensive testing strategies, see:
- [Quality Guide](./quality-guide.md) for quality standards
- Framework-specific testing documentation
