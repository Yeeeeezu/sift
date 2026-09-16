# sift

log file analyzer and filter with a rich terminal ui.

detects log levels automatically, filters by level/regex/key-value fields, and gives you a summary of what's in the log.

---

## usage

```sh
sift app.log                        # dump with level badges
sift app.log -l error               # only errors and above
sift app.log -g "timeout"           # grep: keep matching lines
sift app.log -v "healthcheck"       # ignore: drop matching lines
sift app.log --stats                # append level count bars
sift app.log -n 50                  # last 50 matching lines (like tail)
sift app.log --fields               # show key=value field summary
sift app.log -f status=500          # filter by field value
cat app.log | sift -l warn --stats  # pipe from stdin
```

---

## example output

```
     1   INFO   2024-01-15 09:00:01 server started port=8080
     4   WARN   2024-01-15 09:02:14 high memory usage threshold=85%
    12   ERROR  2024-01-15 09:04:39 database connection failed host=db:5432
    13   ERROR  2024-01-15 09:04:40 retrying attempt=1
    18   FATAL  2024-01-15 09:04:55 giving up, exiting

  ┌──────────────────────────── 5 of 24 lines ────────────────────────────┐
  │  FATAL   1  █
  │  ERROR   2  ██
  │  WARN    1  █
  │  INFO   20  ████████████████████████████████████████              │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## level detection

sift classifies each line by scanning for keywords:

| level | keywords |
|-------|---------|
| FATAL | fatal, crit, critical |
| ERROR | error, err, exception, traceback |
| WARN  | warn, warning |
| DEBUG | debug, dbg |
| TRACE | trace |
| INFO  | everything else |

## flags

| flag | description |
|------|-------------|
| `-l, --level` | minimum level: trace/debug/info/warn/error/fatal |
| `-g, --grep <pattern>` | keep only matching lines (case-insensitive regex) |
| `-v, --ignore <pattern>` | drop matching lines |
| `-f, --field KEY=VALUE` | filter by parsed key=value field (repeatable) |
| `--fields` | show field/value summary instead of lines |
| `--stats` | append level count bar chart |
| `-n, --tail N` | show only last N matching lines |
| `--no-lineno` | hide line numbers |

## structure

```
sift/
  __init__.py    version
  cli.py         click entrypoint
  parser.py      line parser — timestamp extraction, kv parsing, level assignment
  filters.py     filter pipeline (level, grep, ignore, field)
  levels.py      level enum, detection patterns, rich style map
  output.py      rich rendering (lines, summary panel, field table)
pyproject.toml
```

## install

```sh
pip install .
```

requires python 3.9+, click 8+, rich 13+.

## testing

installed and ran against a generated test log with ERROR, WARN, INFO, and DEBUG lines. level detection, grep filter, `--stats` panel, and `--fields` summary all confirmed correct. pipe from stdin confirmed. `--tail` confirmed returning last N lines.

**not tested:** multibyte log files, windows CRLF line endings in the middle of a stream, logs with no recognizable timestamps.

## license

MIT
