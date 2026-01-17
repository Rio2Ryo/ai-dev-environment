---
name: mcp-integration
description: Build and integrate MCP (Model Context Protocol) servers for extending AI capabilities
---

# MCP Integration Skill

This skill guides the creation and integration of MCP servers to extend AI capabilities with custom tools and data sources.

## When to Use This Skill

Use this skill when you need to connect AI assistants to external services, databases, APIs, or custom functionality through the Model Context Protocol.

## MCP Architecture Overview

MCP provides a standardized way for AI assistants to interact with external tools and data sources. An MCP server exposes tools that can be called by AI clients, enabling capabilities like database queries, API calls, file operations, and more.

## Creating an MCP Server

### Basic Structure

An MCP server defines tools with clear names, descriptions, and input schemas. Each tool performs a specific action and returns structured results.

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

server.tool(
  "search_database",
  "Search the database for records matching a query",
  {
    query: { type: "string", description: "Search query" },
    limit: { type: "number", description: "Max results", default: 10 },
  },
  async ({ query, limit }) => {
    const results = await db.search(query, limit);
    return { content: [{ type: "text", text: JSON.stringify(results) }] };
  }
);
```

### Tool Design Principles

Tools should be atomic and focused on a single operation. Provide clear descriptions that help the AI understand when and how to use each tool. Include sensible defaults for optional parameters. Return structured data that's easy for the AI to interpret.

## Configuration

MCP servers are configured in the Claude settings file at `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

## Integration Patterns

### Database Integration

Create tools for common database operations like search, read, and write. Always validate inputs and handle errors gracefully.

### API Wrappers

Wrap external APIs as MCP tools to give AI access to services like GitHub, Slack, or custom internal APIs.

### File System Operations

Provide controlled access to file operations within specific directories. Always validate paths to prevent security issues.

## Testing MCP Servers

Test tools independently before integration. Verify error handling for edge cases. Use the MCP inspector tool to debug communication issues.
