---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

## Process

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools**: Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations.

**Tool Naming and Discoverability**: Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management**: Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data.

**Actionable Error Messages**: Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

Navigate the MCP specification:
- Start with the sitemap: https://modelcontextprotocol.io/sitemap.xml
- Fetch specific pages with `.md` suffix for markdown format

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**
- Language: TypeScript (high-quality SDK support)
- Transport: Streamable HTTP for remote servers, stdio for local servers

**Framework resources:**
- TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- Python SDK: https://github.com/modelcontextprotocol/python-sdk

### Phase 2: Implementation

#### 2.1 Project Structure

**TypeScript:**
```
my-mcp-server/
├── src/
│   ├── index.ts        # Entry point
│   ├── tools/          # Tool implementations
│   ├── resources/      # Resource handlers
│   └── utils/          # Shared utilities
├── package.json
└── tsconfig.json
```

**Python:**
```
my_mcp_server/
├── __init__.py
├── server.py           # Entry point
├── tools/              # Tool implementations
├── resources/          # Resource handlers
└── utils/              # Shared utilities
```

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions
- Add examples in field descriptions

**Output Schema:**
- Define `outputSchema` where possible for structured data
- Use `structuredContent` in tool responses

**Tool Description:**
- Concise summary of functionality
- Parameter descriptions
- Return type schema

**Implementation:**
- Async/await for I/O operations
- Proper error handling with actionable messages
- Support pagination where applicable

**Annotations:**
```typescript
{
  readOnlyHint: true,      // Does not modify data
  destructiveHint: false,  // Does not delete data
  idempotentHint: true,    // Safe to retry
  openWorldHint: false     // Closed set of operations
}
```

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**TypeScript:**
```bash
npm run build
npx @modelcontextprotocol/inspector
```

**Python:**
```bash
python -m py_compile your_server.py
# Test with MCP Inspector
```

## Example: TypeScript MCP Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0",
});

// Define tool input schema
const GetUserSchema = z.object({
  userId: z.string().describe("The unique identifier of the user"),
});

// Register tool
server.registerTool({
  name: "get_user",
  description: "Retrieve user information by ID",
  inputSchema: GetUserSchema,
  annotations: {
    readOnlyHint: true,
    idempotentHint: true,
  },
  handler: async ({ userId }) => {
    try {
      const user = await fetchUser(userId);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(user, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: User not found. Verify the userId is correct.`,
          },
        ],
        isError: true,
      };
    }
  },
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Example: Python MCP Server (FastMCP)

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("my-mcp-server")

class GetUserInput(BaseModel):
    user_id: str = Field(description="The unique identifier of the user")

@mcp.tool()
async def get_user(input: GetUserInput) -> str:
    """Retrieve user information by ID."""
    try:
        user = await fetch_user(input.user_id)
        return json.dumps(user, indent=2)
    except UserNotFoundError:
        raise ValueError(f"User not found. Verify the user_id is correct.")

if __name__ == "__main__":
    mcp.run()
```

## Best Practices

### Tool Design

1. **Single Responsibility**: Each tool does one thing well
2. **Clear Naming**: `{service}_{action}_{resource}` pattern
3. **Helpful Errors**: Include suggestions for resolution
4. **Pagination**: Support for large result sets
5. **Filtering**: Allow narrowing results

### Security

1. **Input Validation**: Validate all inputs
2. **Rate Limiting**: Implement appropriate limits
3. **Authentication**: Secure credential handling
4. **Logging**: Audit trail for sensitive operations

### Performance

1. **Caching**: Cache frequently accessed data
2. **Batching**: Combine related operations
3. **Async**: Non-blocking I/O operations
4. **Timeouts**: Appropriate timeout handling

## Testing Checklist

- [ ] All tools have clear descriptions
- [ ] Input schemas have field descriptions
- [ ] Error messages are actionable
- [ ] Pagination works correctly
- [ ] Authentication is handled securely
- [ ] Rate limits are respected
- [ ] Timeouts are configured
- [ ] Tests cover happy path and error cases
