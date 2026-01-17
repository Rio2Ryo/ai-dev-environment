---
name: react-best-practices
description: React development best practices and patterns for production applications
---

# React Best Practices Skill

This skill provides guidance for building production-quality React applications following modern best practices.

## When to Use This Skill

Use this skill when building React applications, especially when working with Next.js, TypeScript, and modern React patterns.

## Component Architecture

### Composition Over Configuration

Build components that compose well together rather than having many props. Prefer children and render props over complex configuration objects.

```tsx
// Good: Composable
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>

// Avoid: Over-configured
<Card title="Title" body="Content" headerStyle={{}} bodyStyle={{}} />
```

### Single Responsibility

Each component should do one thing well. If a component grows beyond 100-150 lines, consider splitting it.

### Colocation

Keep related code together. Place component-specific hooks, types, and utilities in the same directory as the component.

## State Management

### Local State First

Start with local state (useState, useReducer). Only lift state when necessary. Consider React Context for truly global state before reaching for external libraries.

### Server State

Use React Query or SWR for server state. These handle caching, revalidation, and loading states automatically.

```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
});
```

## Performance Patterns

### Memoization

Use React.memo, useMemo, and useCallback judiciously. Profile before optimizing. Premature optimization often adds complexity without benefit.

### Code Splitting

Use dynamic imports for route-level code splitting. Lazy load heavy components that aren't immediately visible.

```tsx
const HeavyChart = lazy(() => import('./HeavyChart'));
```

## TypeScript Integration

### Strict Types

Enable strict mode in tsconfig.json. Define explicit types for props, state, and API responses. Avoid using `any`.

```tsx
interface UserCardProps {
  user: User;
  onEdit: (id: string) => void;
  isEditable?: boolean;
}
```

## Testing Strategy

Write tests that give confidence without being brittle. Focus on user behavior, not implementation details. Use React Testing Library for component tests.

## Error Handling

Implement Error Boundaries at route and feature levels. Provide meaningful error messages and recovery options to users.
