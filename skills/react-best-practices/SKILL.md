---
name: react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.
---

# React Best Practices

Comprehensive performance optimization guide for React and Next.js applications. Contains 45+ rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## 1. Eliminating Waterfalls (CRITICAL)

### async-parallel
**Use Promise.all() for independent operations**

❌ Bad:
```javascript
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);
```

✅ Good:
```javascript
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
```

### async-suspense-boundaries
**Use Suspense to stream content**

```jsx
<Suspense fallback={<Skeleton />}>
  <SlowComponent />
</Suspense>
```

## 2. Bundle Size Optimization (CRITICAL)

### bundle-barrel-imports
**Import directly, avoid barrel files**

❌ Bad:
```javascript
import { Button, Input, Modal } from '@/components';
```

✅ Good:
```javascript
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
```

### bundle-dynamic-imports
**Use next/dynamic for heavy components**

```javascript
const HeavyChart = dynamic(() => import('./Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false
});
```

### bundle-defer-third-party
**Load analytics/logging after hydration**

```javascript
useEffect(() => {
  import('analytics').then(({ init }) => init());
}, []);
```

## 3. Server-Side Performance (HIGH)

### server-cache-react
**Use React.cache() for per-request deduplication**

```javascript
const getUser = cache(async (id) => {
  return await db.user.findUnique({ where: { id } });
});
```

### server-serialization
**Minimize data passed to client components**

❌ Bad: Passing entire user object
✅ Good: Pass only `{ name, avatar }` needed for display

## 4. Client-Side Data Fetching (MEDIUM-HIGH)

### client-swr-dedup
**Use SWR for automatic request deduplication**

```javascript
const { data, error, isLoading } = useSWR('/api/user', fetcher);
```

## 5. Re-render Optimization (MEDIUM)

### rerender-memo
**Extract expensive work into memoized components**

```jsx
const ExpensiveList = memo(({ items }) => (
  items.map(item => <ExpensiveItem key={item.id} {...item} />)
));
```

### rerender-functional-setstate
**Use functional setState for stable callbacks**

```javascript
// Stable callback - doesn't need to be in deps
const increment = useCallback(() => {
  setCount(c => c + 1);
}, []);
```

### rerender-lazy-state-init
**Pass function to useState for expensive values**

```javascript
const [data] = useState(() => expensiveComputation());
```

## 6. Rendering Performance (MEDIUM)

### rendering-content-visibility
**Use content-visibility for long lists**

```css
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px;
}
```

### rendering-conditional-render
**Use ternary, not && for conditionals**

❌ Bad:
```jsx
{count && <span>{count}</span>}  // Renders "0" when count is 0
```

✅ Good:
```jsx
{count > 0 ? <span>{count}</span> : null}
```

## 7. JavaScript Performance (LOW-MEDIUM)

### js-set-map-lookups
**Use Set/Map for O(1) lookups**

```javascript
const selectedIds = new Set(selected.map(s => s.id));
const isSelected = (id) => selectedIds.has(id);
```

### js-early-exit
**Return early from functions**

```javascript
function process(data) {
  if (!data) return null;
  if (data.cached) return data.cached;
  // ... expensive processing
}
```

## 8. Advanced Patterns (LOW)

### advanced-use-latest
**useLatest for stable callback refs**

```javascript
function useLatest(value) {
  const ref = useRef(value);
  ref.current = value;
  return ref;
}
```

## Quick Checklist

Before submitting React/Next.js code:

- [ ] No sequential awaits for independent data
- [ ] Heavy components use dynamic imports
- [ ] Direct imports (no barrel files)
- [ ] Server components minimize client data
- [ ] Expensive renders are memoized
- [ ] Lists use content-visibility or virtualization
- [ ] Lookups use Set/Map instead of array.find()

## References

- [Vercel Engineering Blog](https://vercel.com/blog)
- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org/docs)
