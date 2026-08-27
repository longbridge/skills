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

`order buy`, `order sell`, `order cancel` and `order replace` **place nothing on
the first run**. Without `--execute` they are dry runs: the CLI validates every
argument, prints the exact order (buy/sell previews also show the last traded
price and estimated amount; cancel/replace show the order being targeted), and
contacts no exchange.

Never add `--execute` on your own initiative. The required sequence is:

1. Run the command **without** `--execute`.
2. Show the returned preview to the user.
3. Only after the user explicitly confirms **that exact order**, re-run the
   identical command with `--execute`.

```bash
# 1. Preview — nothing is placed
longbridge order buy TSLA.US 100 --price 250.00 --format json

# 2. …show the preview, get an explicit "yes" from the user…

# 3. Place it
longbridge order buy TSLA.US 100 --price 250.00 --execute
```

The JSON dry run returns `{"dry_run": true, ..., "message": "..."}` — relay it
rather than summarising it away. The legacy `-y` / `--yes` flag has been removed;
if you find it in an old script or example, it is wrong.

The same gate applies to every `grid` write command (`grid submit`, `replace`,
`cancel`, `suspend`, `restart`) — a live grid keeps placing orders on its own,
so it deserves at least as much care as a single order.

## Usage

```bash
# Run with JSON output for AI agents
longbridge order --format json

# See all options
longbridge order --help
```
