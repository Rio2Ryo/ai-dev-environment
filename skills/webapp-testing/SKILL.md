---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Start server first, then run Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Basic Playwright Script Template

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Navigate to the app
    page.goto('http://localhost:3000')
    
    # CRITICAL: Wait for JS to execute
    page.wait_for_load_state('networkidle')
    
    # Your automation logic here
    page.click('button[type="submit"]')
    page.fill('input[name="email"]', 'test@example.com')
    
    # Take screenshot for verification
    page.screenshot(path='screenshot.png', full_page=True)
    
    browser.close()
```

## Reconnaissance-Then-Action Pattern

### 1. Inspect rendered DOM

```python
# Take screenshot for visual inspection
page.screenshot(path='/tmp/inspect.png', full_page=True)

# Get page content
content = page.content()

# List all buttons
buttons = page.locator('button').all()
for btn in buttons:
    print(btn.text_content())
```

### 2. Identify selectors from inspection results

```python
# Common selector strategies
page.locator('text=Submit')           # By text content
page.locator('role=button')           # By ARIA role
page.locator('#submit-btn')           # By ID
page.locator('.btn-primary')          # By class
page.locator('[data-testid="submit"]') # By test ID (recommended)
```

### 3. Execute actions using discovered selectors

```python
# Click actions
page.click('button:has-text("Submit")')
page.click('[data-testid="login-button"]')

# Form filling
page.fill('input[name="username"]', 'testuser')
page.fill('input[type="password"]', 'password123')

# Select dropdown
page.select_option('select#country', 'JP')

# Check/uncheck
page.check('input[type="checkbox"]')
```

## Common Pitfalls

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps

✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

❌ **Don't** use hardcoded waits like `time.sleep(5)`

✅ **Do** use smart waits:
```python
page.wait_for_selector('.loaded')
page.wait_for_load_state('networkidle')
page.wait_for_function('window.appReady === true')
```

## Console Log Capture

```python
# Capture console messages
page.on('console', lambda msg: print(f'Console: {msg.text}'))

# Capture errors
page.on('pageerror', lambda err: print(f'Error: {err}'))
```

## Screenshot Strategies

```python
# Full page screenshot
page.screenshot(path='full.png', full_page=True)

# Element screenshot
page.locator('.hero-section').screenshot(path='hero.png')

# Viewport only
page.screenshot(path='viewport.png')

# With specific viewport size
page.set_viewport_size({'width': 375, 'height': 667})  # Mobile
page.screenshot(path='mobile.png')
```

## Testing Forms

```python
# Fill and submit form
page.fill('#email', 'test@example.com')
page.fill('#password', 'secure123')
page.click('button[type="submit"]')

# Wait for navigation after submit
page.wait_for_url('**/dashboard')

# Verify success
assert page.locator('.welcome-message').is_visible()
```

## Testing API Responses

```python
# Intercept and verify API calls
with page.expect_response('**/api/users') as response_info:
    page.click('#load-users')

response = response_info.value
assert response.status == 200
data = response.json()
assert len(data['users']) > 0
```

## Best Practices

1. **Use sync_playwright()** for synchronous scripts
2. **Always close the browser** when done
3. **Use descriptive selectors**: `text=`, `role=`, CSS selectors, or IDs
4. **Add appropriate waits**: `wait_for_selector()` or `wait_for_timeout()`
5. **Use data-testid attributes** for reliable element selection
6. **Run headless in CI**, headed locally for debugging

## Debugging Tips

```python
# Run headed (visible browser)
browser = p.chromium.launch(headless=False)

# Slow down actions
browser = p.chromium.launch(headless=False, slow_mo=500)

# Pause for debugging
page.pause()  # Opens Playwright Inspector

# Record video
context = browser.new_context(record_video_dir='videos/')
```
