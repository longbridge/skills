# order

```
Order management: list, detail, buy, sell, cancel, replace, executions

Without a subcommand, lists today's orders (or historical with --history). Example: longbridge order Example: longbridge order --history --start 2024-01-01 --symbol TSLA.US Example: longbridge order detail 20240101-123456789 Example: longbridge order buy TSLA.US 100 --price 250.00 Example: longbridge order sell TSLA.US 100 --price 260.00 Example: longbridge order cancel 20240101-123456789 Example: longbridge order replace 20240101-123456789 --qty 200 --price 255.00 Example: longbridge order executions --history --start 2024-01-01

Usage: longbridge order [OPTIONS] [COMMAND]

Commands:
  detail      Full detail for a single order including charges and history
  executions  Today's trade executions (fills), or historical with --history
  buy         Preview a buy order (dry run); add --execute to actually place it
  sell        Preview a sell order (dry run); add --execute to actually place it
  cancel      Preview cancelling a pending order (dry run); add --execute to cancel it
  replace     Preview modifying a pending order (dry run); add --execute to apply it
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
          US accounts only: filter by direction (buy | sell)

      --page <PAGE>
          US accounts only: page number (default: 1)
          
          [default: 1]

      --limit <LIMIT>
          US accounts only: page size (default: 20)
          
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

## Placing, cancelling or modifying an order — MANDATORY

`order buy`, `order sell`, `order cancel`, `order replace` and every `grid`
write command preview by default. The first run reaches no exchange: it prints
the order for review, and ends with the exact command that would carry it out.

1. Run the command.
2. Show the preview to the user and ask them to confirm.
3. Only after they explicitly confirm, run the command the preview printed —
   verbatim.

Never assemble that second command yourself, and never reuse one across
different orders.

## Usage

```bash
# Run with JSON output for AI agents
longbridge order --format json

# See all options
longbridge order --help
```
