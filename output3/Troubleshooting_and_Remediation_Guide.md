# Troubleshooting and Remediation Guide

## Common Issues & Resolutions

### 1. Incorrect Discount Calculation
- **Symptom:** Output does not match expected values.
- **Resolution:**
  - Verify logic for customer type and amount thresholds.
  - Ensure case-insensitive string comparison for customer types.
  - Check for correct application of additional discount for amounts > 10000.

### 2. Negative or Zero Amounts
- **Symptom:** Final amount is negative or not zero for non-positive inputs.
- **Resolution:**
  - Confirm the final amount is set to zero if calculation yields a negative value.
  - Add/validate test cases for negative and zero amounts.

### 3. Unrecognized Customer Types
- **Symptom:** Unexpected discount or error when passing unknown customer type.
- **Resolution:**
  - Default discount should be 0 for unrecognized types.
  - Add/validate test cases for unknown customer types.

### 4. Test Failures
- **Symptom:** Automated tests fail during CI/CD pipeline execution.
- **Resolution:**
  - Review test suite for up-to-date expected values.
  - Ensure migrated logic is deployed before running tests.
  - Check for build or dependency issues.

## Remediation Steps
1. Reproduce the issue with failing input.
2. Trace execution in the `calculateDiscount` method.
3. Compare actual logic with business requirements/specifications.
4. Update code/test suite as necessary and rerun tests.
5. Commit and push changes; verify status via GitHub Actions or CI logs.

## Reporting & Support
- Report unresolved issues by creating a GitHub Issue in the repository.
- Attach test results and logs for faster resolution.

---
