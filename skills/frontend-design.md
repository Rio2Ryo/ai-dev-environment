---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics
---

# Frontend Design Skill

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics.

## When to Use This Skill

Use this skill when:
- Creating new web interfaces, landing pages, or dashboards
- Designing React/Next.js components
- Building UI with Tailwind CSS
- Need to ensure high-quality, professional design output

## Design Principles

### 1. Avoid Generic AI Aesthetics
- No excessive gradients without purpose
- No overuse of rounded corners on everything
- No generic stock-photo-like hero sections
- No meaningless decorative elements

### 2. Typography Excellence
- Use a clear type hierarchy (display, heading, body, caption)
- Limit to 2-3 font families maximum
- Ensure proper line-height (1.4-1.6 for body text)
- Use appropriate font weights for emphasis

### 3. Color Strategy
- Start with a limited palette (2-3 colors + neutrals)
- Use color purposefully for hierarchy and action
- Ensure WCAG AA contrast ratios minimum
- Consider dark mode from the start

### 4. Spacing System
- Use consistent spacing scale (4, 8, 12, 16, 24, 32, 48, 64, 96)
- Apply generous whitespace for breathing room
- Maintain consistent padding/margin patterns

### 5. Component Design
- Design mobile-first, then scale up
- Use semantic HTML elements
- Ensure interactive states (hover, focus, active, disabled)
- Add subtle animations for feedback (150-300ms)

## Implementation Guidelines

### React/Next.js
```tsx
// Use composition over configuration
// Prefer small, focused components
// Use TypeScript for type safety
// Implement proper error boundaries
```

### Tailwind CSS
```css
/* Use @apply sparingly */
/* Prefer utility classes in JSX */
/* Create custom design tokens in tailwind.config.js */
/* Use arbitrary values only when necessary */
```

### Accessibility
- All interactive elements must be keyboard accessible
- Use proper ARIA labels and roles
- Ensure focus indicators are visible
- Test with screen readers

## Quality Checklist

Before completing any frontend work:
- [ ] Responsive on mobile, tablet, desktop
- [ ] All interactive states implemented
- [ ] Keyboard navigation works
- [ ] Color contrast passes WCAG AA
- [ ] No layout shifts on load
- [ ] Images optimized and lazy-loaded
- [ ] Forms have proper validation feedback
