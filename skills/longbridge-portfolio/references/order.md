# order

```
Order management: list, detail, buy, sell, cancel, replace, executions

Behavior adapts to your account's region automatically; you never pass a region. --action/--page/--limit apply only to US accounts.

Without a subcommand, lists today's orders (or historical with --history). Example: longbridge order Example: longbridge order --history --start 2024-01-01 --symbol TSLA.US Example: longbridge order detail 20240101-123456789 Example: longbridge order buy TSLA.US 100 --price 250.00 Example: longbridge order sell TSLA.US 100 --price 260.00 Example: longbridge order cancel 20240101-123456789 Example: longbridge order replace 20240101-123456789 --qty 200 --price 255.00 Example: longbridge order executions --history --start 2024-01-01

Usage: longbridge order [OPTIONS] [COMMAND]

Commands:
  detail      Full detail for a single order including charges and history
  executions  AP accounts only: today's trade executions (fills), or the full history with --history
  buy         Preview a buy order (dry run); add --execute <CODE> to place it
  sell        Preview a sell order (dry run); add --execute <CODE> to place it
  cancel      Preview cancelling a pending order (dry run); add --execute <CODE> to cancel it
  replace     Preview modifying a pending order (dry run); add --execute <CODE> to apply it
  help        Print this message or the help of the given subcommand(s)

Options:
      --history
          Return historical orders instead of today's (list mode only)

      --start <START>
          Filter start date/time (local YYYY-MM-DD, local "YYYY-MM-DD HH:MM", or RFC 3339)

      --end <END>
          Filter end date/time (local YYYY-MM-DD, local "YYYY-MM-DD HH:MM", or RFC 3339)

      --symbol <SYMBOL>
          Filter by symbol (e.g. TSLA.US)

      --action <DIRECTION>
          US accounts only: filter by direction (buy | sell). Ignored for AP accounts (the region is inferred from your account — do not pass it)

      --page <PAGE>
          US accounts only: page number (default: 1). Ignored for AP accounts (the region is inferred from your account — do not pass it)
          
          [default: 1]

      --limit <LIMIT>
          US accounts only: page size (default: 20). Ignored for AP accounts (the region is inferred from your account — do not pass it)
          
          [default: 20]

      --format <FORMAT>
          Output format: 'pretty' for human-readable, 'json' for AI agents and scripting
          
          [default: pretty]
          [possible values: table, json]

  -v, --verbose
          Print verbose request info (host, elapsed) to stderr, prefixed with `*` like curl -v

      --lang <LANG>
          Language for content fetched from longbridge.com: zh-CN or en. Defaults to system LANG env var, then en

      --schema
          Show response fields for this command and exit

  -h, --help
          Print help (see a summary with '-h')
```

## Usage

```bash
# Run with JSON output for AI agents
longbridge order --format json

# See all options
longbridge order --help
```

> ⚠️ **Mutating command** — `order buy`, `order sell`, `order cancel`, `order replace` modify account state. Always present a preview to the user and wait for explicit confirmation before executing.

## Placing, cancelling or changing an order

Order commands are **dry runs by default**. Without the execute flag, `buy` / `sell` / `cancel` / `replace` only print a preview and a confirmation code; nothing is sent.

1. Run the command without the execute flag and show the user the preview.
2. Wait for an explicit confirmation from the user.
3. Re-run the **identical** command with `--execute <CODE>`, using the code from the preview. Check `longbridge order buy --help` if the flag has changed.

Never add the execute flag before the user has confirmed, and never reuse a code from a different preview.

The confirmation code is single-use, expires 10 minutes after the preview, and is tied to that exact request — changing any field invalidates it. If the code is rejected or has expired, re-run the preview, show it to the user again and get a fresh confirmation.
