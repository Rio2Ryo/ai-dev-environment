---
name: systematic-debugging
description: Methodical problem-solving approach for debugging code issues. Use this skill when encountering errors, unexpected behavior, or when code doesn't work as expected. Provides a structured framework for identifying root causes and implementing fixes.
---

# Systematic Debugging

A structured approach to debugging that ensures thorough investigation and reliable fixes.

## The Debugging Framework

### Phase 1: Understand the Problem

Before touching any code:

1. **Reproduce the issue**
   - Can you consistently trigger the bug?
   - What are the exact steps to reproduce?
   - Document the expected vs actual behavior

2. **Gather information**
   - Error messages (full stack trace)
   - Console logs
   - Network requests/responses
   - Environment details (OS, browser, Node version)

3. **Define the scope**
   - When did it start happening?
   - What changed recently?
   - Does it happen in all environments?

### Phase 2: Isolate the Problem

```
Start with the symptom
    │
    ▼
Identify the component/module involved
    │
    ▼
Narrow down to specific function/method
    │
    ▼
Find the exact line causing the issue
```

**Techniques:**

1. **Binary search debugging**
   - Comment out half the code
   - If bug persists, it's in the remaining half
   - Repeat until isolated

2. **Add strategic logging**
   ```javascript
   console.log('=== DEBUG: functionName ===');
   console.log('Input:', JSON.stringify(input, null, 2));
   console.log('State:', JSON.stringify(state, null, 2));
   ```

3. **Use debugger breakpoints**
   ```javascript
   debugger; // Pause execution here
   ```

### Phase 3: Form Hypotheses

Based on gathered information, form specific hypotheses:

**Good hypothesis format:**
> "The bug occurs because [specific cause] which leads to [observed symptom] when [specific condition]"

**Example:**
> "The bug occurs because the API response is cached, which leads to stale data being displayed when the user navigates back to the page"

### Phase 4: Test Hypotheses

For each hypothesis:

1. **Design a test** that would prove/disprove it
2. **Execute the test** with minimal changes
3. **Document the result**
4. **Move to next hypothesis** if disproven

### Phase 5: Implement the Fix

Once root cause is identified:

1. **Write a failing test** that reproduces the bug
2. **Implement the minimal fix**
3. **Verify the test passes**
4. **Check for regressions**
5. **Document the fix**

## Common Bug Categories

### 1. State Management Issues

**Symptoms:**
- UI shows stale data
- Actions don't reflect immediately
- Race conditions

**Debug approach:**
```javascript
// Log state changes
useEffect(() => {
  console.log('State changed:', state);
}, [state]);
```

### 2. Async/Timing Issues

**Symptoms:**
- Works sometimes, fails others
- Order-dependent failures
- "Cannot read property of undefined"

**Debug approach:**
```javascript
// Add timestamps to async operations
console.log(`[${Date.now()}] Starting fetch`);
const data = await fetch(url);
console.log(`[${Date.now()}] Fetch complete`);
```

### 3. Type/Data Issues

**Symptoms:**
- NaN, undefined, null errors
- Wrong data format
- Missing properties

**Debug approach:**
```javascript
// Validate data at boundaries
function processUser(user) {
  console.assert(user != null, 'User is null');
  console.assert(typeof user.id === 'number', 'User ID is not a number');
  // ...
}
```

### 4. Environment/Configuration Issues

**Symptoms:**
- Works locally, fails in production
- Works for some users, not others
- Intermittent failures

**Debug approach:**
```javascript
// Log environment details
console.log('Environment:', {
  nodeEnv: process.env.NODE_ENV,
  apiUrl: process.env.API_URL,
  version: process.env.VERSION
});
```

## Debugging Tools by Context

### Browser JavaScript
- Chrome DevTools (Console, Sources, Network)
- React DevTools
- Vue DevTools
- Redux DevTools

### Node.js
- `node --inspect` + Chrome DevTools
- VS Code debugger
- `console.log` with structured output

### API/Network
- Browser Network tab
- Postman/Insomnia
- `curl` commands
- Proxy tools (Charles, Fiddler)

### Database
- Query logs
- EXPLAIN ANALYZE
- Database GUI tools

## Debug Logging Best Practices

```javascript
// Use structured logging
const debug = {
  log: (context, message, data = {}) => {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      context,
      message,
      ...data
    }));
  }
};

// Usage
debug.log('UserService', 'Fetching user', { userId: 123 });
```

## Post-Debugging Checklist

After fixing a bug:

- [ ] Root cause is documented
- [ ] Fix is minimal and focused
- [ ] Test added to prevent regression
- [ ] Related code reviewed for similar issues
- [ ] Documentation updated if needed
- [ ] Team notified of fix (if applicable)

## Anti-Patterns to Avoid

❌ **Shotgun debugging** - Making random changes hoping something works

❌ **Blame-first debugging** - Assuming it's someone else's code/library

❌ **Fix-and-forget** - Not understanding why the fix works

❌ **Over-engineering** - Adding complexity to "prevent" future bugs

✅ **Always understand the root cause before implementing a fix**
