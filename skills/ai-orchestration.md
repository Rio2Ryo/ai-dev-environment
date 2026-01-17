---
name: ai-orchestration
description: Orchestrate multiple AI models and tools for optimal cost and performance
---

# AI Orchestration Skill

This skill provides guidance on selecting and orchestrating multiple AI models and tools to optimize for cost, performance, and quality.

## When to Use This Skill

Use this skill when deciding which AI model or tool to use for a given task, or when designing systems that leverage multiple AI services.

## Model Selection Strategy

### Cost-Optimized Selection

For simple tasks like code formatting, basic explanations, or straightforward generation, use lower-cost models first. Gemini's free tier provides 1,000 requests per day, making it ideal for high-volume, simple tasks. Grok Code Fast 1 offers excellent speed at $0.20/M input tokens.

### Quality-Optimized Selection

For complex reasoning, algorithm design, or nuanced code review, use more capable models. GPT-5.2, Claude Opus, and Grok-4 excel at tasks requiring deep understanding and sophisticated output.

### Task-Based Routing

| Task Type | Primary Choice | Fallback |
|-----------|---------------|----------|
| Simple code generation | Gemini CLI | Grok Code Fast 1 |
| Complex algorithms | GPT-5.2 Codex | Claude Opus |
| Code review | Grok Code Fast 1 | Codex |
| Debugging | Claude Code | Gemini CLI |
| Documentation | Gemini | GPT-4o |
| Research/Search | Grok (Web Search) | Gemini (Google Search) |

## Orchestration Patterns

### Sequential Pipeline

Use one model's output as input to another. For example, use a fast model for initial code generation, then a more capable model for review and refinement.

### Parallel Execution

For independent subtasks, run multiple models in parallel and aggregate results. This is useful for gathering diverse perspectives or validating outputs.

### Fallback Chain

Configure automatic fallback when a model fails or returns unsatisfactory results. Start with the most cost-effective option and escalate as needed.

## Implementation with Manus

Manus serves as the central orchestrator, routing tasks to appropriate AI services based on task characteristics. The environment includes:

- **ANTHROPIC_API_KEY**: Access to Claude models
- **OPENAI_API_KEY**: Access to GPT models and Codex
- **GEMINI_API_KEY**: Access to Gemini models
- **XAI_API_KEY**: Access to Grok models

## Cost Monitoring

Track token usage across all services. Set up alerts for unusual consumption patterns. Regularly review which models are being used and optimize routing rules based on actual performance data.
