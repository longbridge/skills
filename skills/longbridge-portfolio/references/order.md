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

## Two-step execution gate — MANDATORY

`order buy`, `order sell`, `order cancel`, `order replace` and every `grid`
write command place nothing on the first run. Without `--execute` they print a
preview and contact no exchange.

1. Run the command **without** `--execute`.
2. Show the preview to the user.
3. Only after they explicitly confirm, run the command the preview printed —
   it carries the confirmation code `--execute` needs.

Never construct that command yourself, and never carry a code over to a
different order.

## Usage

```bash
# Run with JSON output for AI agents
longbridge order --format json

# See all options
longbridge order --help
```
