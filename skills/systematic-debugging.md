---
name: systematic-debugging
description: Four-phase systematic approach to root cause investigation and bug fixing
---

# Systematic Debugging Skill

This skill provides a structured four-phase approach to debugging that ensures thorough root cause analysis before implementing fixes.

## When to Use This Skill

Use this skill when encountering bugs, errors, or unexpected behavior in code. This approach prevents superficial fixes that don't address underlying issues.

## Phase 1: Reproduce and Isolate

Before attempting any fix, reliably reproduce the issue. Document the exact steps, inputs, and environment conditions that trigger the bug. Create a minimal reproduction case by removing unrelated code until you have the smallest example that still exhibits the problem.

Questions to answer:
- Can I reproduce this consistently?
- What are the exact steps to trigger it?
- What is the expected vs actual behavior?
- In what environments does this occur?

## Phase 2: Gather Evidence

Collect data about the bug without making assumptions. Use logging, debuggers, and monitoring tools to understand what's actually happening versus what you think is happening.

Evidence gathering techniques:
- Add strategic console.log or debugger statements
- Check network requests and responses
- Review error messages and stack traces
- Examine state at various points in execution
- Compare working vs non-working scenarios

## Phase 3: Form and Test Hypotheses

Based on evidence, form specific hypotheses about the root cause. Test each hypothesis systematically rather than making random changes.

For each hypothesis:
1. State the hypothesis clearly
2. Predict what you would observe if it's correct
3. Design a test to validate or invalidate it
4. Execute the test and record results
5. Either confirm or move to next hypothesis

## Phase 4: Implement and Verify Fix

Once root cause is identified, implement a targeted fix. The fix should address the root cause, not just symptoms.

Verification checklist:
- Does the fix resolve the original issue?
- Does it handle edge cases?
- Are there similar issues elsewhere in the codebase?
- Have you added tests to prevent regression?
- Is the fix documented if non-obvious?

## Anti-Patterns to Avoid

Avoid making random changes hoping something works. Don't assume you know the cause without evidence. Never commit a fix without verifying it actually solves the problem. Don't ignore the root cause in favor of quick workarounds.
