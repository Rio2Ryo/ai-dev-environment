---
name: code-review
description: Perform thorough code reviews focusing on correctness, performance, security, and maintainability. Use this skill when reviewing pull requests, auditing code quality, or providing feedback on implementations.
---

# Code Review Skill

A systematic approach to reviewing code that ensures quality, security, and maintainability.

## Review Process

### 1. Understand the Context

Before reviewing code:
- Read the PR description/ticket
- Understand the problem being solved
- Check related documentation
- Review any linked issues

### 2. High-Level Review

First pass - understand the overall approach:
- Does the solution make sense?
- Is the architecture appropriate?
- Are there simpler alternatives?

### 3. Detailed Review

Second pass - examine implementation:
- Correctness
- Performance
- Security
- Maintainability
- Testing

## Review Checklist

### Correctness

- [ ] Logic is correct and handles edge cases
- [ ] Error handling is appropriate
- [ ] Null/undefined checks where needed
- [ ] Boundary conditions handled
- [ ] Race conditions considered (async code)

### Performance

- [ ] No unnecessary re-renders (React)
- [ ] Efficient data structures used
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Large lists virtualized
- [ ] Heavy operations debounced/throttled

### Security

- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Sensitive data not logged
- [ ] Authentication/authorization checked
- [ ] Secrets not hardcoded

### Maintainability

- [ ] Code is readable and self-documenting
- [ ] Functions are single-purpose
- [ ] No magic numbers/strings
- [ ] Appropriate abstractions
- [ ] Consistent naming conventions
- [ ] No dead code

### Testing

- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests cover error cases
- [ ] Tests are readable
- [ ] No flaky tests

## Common Issues by Language

### JavaScript/TypeScript

```javascript
// ❌ Bad: Type coercion issues
if (value == null) { }

// ✅ Good: Explicit checks
if (value === null || value === undefined) { }
```

```javascript
// ❌ Bad: Floating point comparison
if (0.1 + 0.2 === 0.3) { }

// ✅ Good: Epsilon comparison
if (Math.abs((0.1 + 0.2) - 0.3) < Number.EPSILON) { }
```

```javascript
// ❌ Bad: Array mutation
const sorted = arr.sort();

// ✅ Good: Immutable operation
const sorted = [...arr].sort();
```

### React

```jsx
// ❌ Bad: Missing key
{items.map(item => <Item {...item} />)}

// ✅ Good: Unique key
{items.map(item => <Item key={item.id} {...item} />)}
```

```jsx
// ❌ Bad: Object in dependency array
useEffect(() => {
  fetchData(options);
}, [options]); // options is new object every render

// ✅ Good: Primitive dependencies
useEffect(() => {
  fetchData({ page, limit });
}, [page, limit]);
```

### Python

```python
# ❌ Bad: Mutable default argument
def append_to(element, to=[]):
    to.append(element)
    return to

# ✅ Good: None default
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```

### SQL

```sql
-- ❌ Bad: SQL injection risk
query = f"SELECT * FROM users WHERE id = {user_id}"

-- ✅ Good: Parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

## Feedback Guidelines

### Be Constructive

❌ "This code is bad"
✅ "Consider using X instead of Y because [specific reason]"

### Be Specific

❌ "This could be improved"
✅ "This function has O(n²) complexity. Using a Set would make it O(n)"

### Explain Why

❌ "Don't use var"
✅ "Use const/let instead of var to prevent hoisting issues and enable block scoping"

### Suggest Solutions

❌ "This is wrong"
✅ "This could cause a race condition. Consider using a mutex or queue"

### Prioritize Feedback

Use labels to indicate severity:
- 🔴 **Blocker**: Must fix before merge
- 🟡 **Suggestion**: Should consider fixing
- 🟢 **Nit**: Minor improvement, optional

## Review Comment Templates

### Security Issue
```
🔴 **Security**: This endpoint doesn't validate user permissions.
An attacker could access other users' data by changing the ID.

Suggested fix: Add authorization check before returning data.
```

### Performance Issue
```
🟡 **Performance**: This query runs inside a loop, causing N+1 queries.

Suggested fix: Batch the queries or use eager loading.
```

### Code Quality
```
🟢 **Nit**: Consider extracting this logic into a helper function
for better readability and reusability.
```

## Self-Review Before Submitting

Before requesting review:
- [ ] Code compiles/runs without errors
- [ ] All tests pass
- [ ] Linter warnings addressed
- [ ] PR description is clear
- [ ] Changes are focused (single concern)
- [ ] No debugging code left in
