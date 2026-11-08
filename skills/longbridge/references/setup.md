# Longbridge Setup & Authentication

## CLI Installation

> **Quickest:** run the installer bundled with the `longbridge` skill — `sh scripts/install-cli.sh` (macOS / Linux) or `powershell -ExecutionPolicy Bypass -File scripts\install-cli.ps1` (Windows), paths relative to the `longbridge` skill directory. Confirm with the user before installing.

```bash
# macOS (Homebrew — recommended)
brew install --cask longbridge/tap/longbridge-terminal
```

Windows (Scoop):

```powershell
scoop install https://open.longbridge.com/longbridge/longbridge-terminal/longbridge.json
```

Other platforms: download a release binary from <https://github.com/longbridge/longbridge-terminal/releases> and put `longbridge` on your `PATH`.

Authenticate:

```bash
longbridge auth login
```

## CLI Update

```bash
# Built-in updater
longbridge update
```

## MCP (for AI tools — no code)

```bash
# Claude Code
claude mcp add longbridge https://mcp.longbridge.com
```

First tool call triggers an OAuth browser flow. See [references/mcp.md](references/mcp.md) for Cursor, ChatGPT, Zed.

## Revoking Authorization

To revoke access, go to your Longbridge account → Security Settings → manage authorized apps.

## Authentication

All tools use **OAuth 2.0** — no manual token or API key management needed.

Credentials are handled entirely by the OAuth flow (`longbridge auth login` for the CLI, the browser prompt on first MCP call). Never read, print, or copy token files.

**Register OAuth client:** POST `https://openapi.longbridge.com/oauth2/register`

## Rate Limits

- REST API: max **10 calls/second**
- SDK auto-refreshes OAuth tokens
- WebSocket subscriptions: subject to quote package limits
