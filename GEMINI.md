# AI Development Environment - Project Context

This is a smartphone-first AI development environment that orchestrates multiple AI models for optimal cost and performance.

## Project Structure

```
ai-dev-environment/
├── scripts/           # Python scripts for AI orchestration
│   ├── ai_orchestrator.py    # Main orchestrator
│   ├── frontend_helper.py    # Frontend development helper
│   └── debug_helper.py       # Debugging helper
├── skills/            # Custom Claude Code skills
├── config/            # Configuration files
│   └── settings.json  # Environment settings
└── docs/              # Documentation
```

## Available AI Services

This environment has access to the following AI services via environment variables:

- **Anthropic (Claude)**: ANTHROPIC_API_KEY
- **OpenAI (GPT/Codex)**: OPENAI_API_KEY
- **Google (Gemini)**: GEMINI_API_KEY
- **xAI (Grok)**: XAI_API_KEY

## CLI Tools Installed

- `claude` (v2.1.11) - Claude Code CLI
- `gemini` (v0.24.0) - Gemini CLI
- `codex` (v0.87.0) - OpenAI Codex CLI

## Task Routing Strategy

| Task Type | Primary Model | Fallback |
|-----------|--------------|----------|
| Simple code | Gemini | Grok Code Fast |
| Complex algorithms | GPT-5 | Claude Opus |
| Code review | Grok Code Fast | Codex |
| Debugging | Claude | Gemini |
| Frontend | Claude | GPT-5 |
| Documentation | Gemini | GPT-4o |
| Research | Grok (Web) | Gemini (Search) |

## Skills Available

The following custom skills are loaded from `~/.claude/skills/`:

1. **frontend-design** - Production-grade UI development
2. **react-best-practices** - React patterns and practices
3. **systematic-debugging** - Four-phase debugging methodology
4. **mcp-integration** - MCP server development
5. **ai-orchestration** - Multi-model orchestration

## Usage Examples

### Generate a React component
```bash
python3 scripts/frontend_helper.py generate "A responsive navigation bar with dark mode toggle"
```

### Analyze an error
```bash
python3 scripts/debug_helper.py analyze "TypeError: Cannot read property 'map' of undefined"
```

### Use the orchestrator directly
```bash
python3 scripts/ai_orchestrator.py --check  # Check available models
python3 scripts/ai_orchestrator.py "Write a function to sort an array"
```

## Development Guidelines

When working on this project:

1. Use the appropriate AI model for each task type
2. Leverage the installed skills for consistent quality
3. Prefer free-tier models (Gemini) for simple tasks
4. Use more capable models (Claude, GPT-5) for complex work
5. Always run tests before committing changes
