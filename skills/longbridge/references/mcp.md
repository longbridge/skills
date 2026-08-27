# MCP Server

Longbridge provides MCP (Model Context Protocol) support in two modes: a hosted cloud service and a self-hosted binary.

## Hosted MCP Service

**Endpoint:** `https://mcp.longbridge.com`

No API keys needed — uses OAuth 2.1. The AI client handles the browser authorization flow automatically.

### Client Configuration

Add to MCP config in any compatible client:

```json
{
  "mcpServers": {
    "longbridge": {
      "url": "https://mcp.longbridge.com"
    }
  }
}
```

**Per-client setup:**

- **Cursor**: Settings → MCP Servers → Add Remote MCP Server
- **Claude Code**: `claude mcp add longbridge https://mcp.longbridge.com`
- **ChatGPT**: Settings → Connectors
- **Zed**: `context_servers` in `settings.json`
- **Cherry Studio**: Settings → MCP Servers → Add (requires latest version for OAuth support)

### OAuth Authorization Flow

1. Add the config and call any tool — this triggers the OAuth flow
2. Client opens a browser tab to Longbridge login & consent page
3. Sign in with your Longbridge account and approve scopes
4. Credentials are stored by the client; tokens refresh automatically
5. To revoke: Longbridge account → Security Settings

### Security Recommendations

- Only approve scopes required for the task (least privilege)
- Periodically review and revoke unused authorizations

### Order Execution Gate

The money-moving tools — `submit_order`, `cancel_order`, `replace_order` and the
grid writes — do nothing on the first call. Without `execute` they return a
preview and a `confirmation_code`.

1. Call the tool **without** `execute`.
2. Show the returned `preview` to the user.
3. Only after they explicitly confirm, call again with `execute` set to that
   `confirmation_code`.

Never invent a code, and never carry one over to a different order.
