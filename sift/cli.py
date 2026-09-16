import sys
import click
from rich.console import Console

from .parser import parse_stream
from .filters import apply_filters, count_by_level
from .levels import Level
from .output import console, print_lines, print_summary, print_fields

LEVEL_CHOICE = click.Choice(['trace', 'debug', 'info', 'warn', 'error', 'fatal'], case_sensitive=False)
LEVEL_MAP = {
    'trace': Level.TRACE, 'debug': Level.DEBUG, 'info':  Level.INFO,
    'warn':  Level.WARN,  'error': Level.ERROR,  'fatal': Level.FATAL,
}

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument('file', type=click.File('r', encoding='utf-8', errors='replace'), default='-')
@click.option('-l', '--level', 'min_level', type=LEVEL_CHOICE, default=None,
              help='show only lines at or above this level')
@click.option('-g', '--grep', default=None, help='keep only lines matching pattern')
@click.option('-v', '--ignore', default=None, help='drop lines matching pattern')
@click.option('-f', '--field', 'fields', multiple=True, metavar='KEY=VALUE',
              help='filter by key=value field (repeatable)')
@click.option('--fields', 'show_fields', is_flag=True, help='show field summary instead of lines')
@click.option('--stats', is_flag=True, help='append level counts summary')
@click.option('-n', '--tail', type=int, default=None,
              help='show only last N matching lines')
@click.option('--no-lineno', is_flag=True, help='hide line numbers')
def main(file, min_level, grep, ignore, fields, show_fields, stats, tail, no_lineno):
    """log file analyzer. reads FILE (or stdin) and filters / summarizes log lines."""
    try:
        raw_lines = file.readlines()
    except Exception as e:
        console.print(f"[red]error reading input: {e}[/red]")
        sys.exit(1)

    parsed = parse_stream(raw_lines)
    total  = len(parsed)

    field_filter = {}
    for f in fields:
        if '=' in f:
            k, _, v = f.partition('=')
            field_filter[k.strip()] = v.strip()

    filtered = apply_filters(
        parsed,
        min_level=LEVEL_MAP.get(min_level) if min_level else None,
        grep=grep,
        ignore=ignore,
        field_filter=field_filter or None,
    )

    if tail is not None:
        filtered = filtered[-tail:]

    if show_fields:
        print_fields(filtered)
        return

    print_lines(filtered, show_lineno=not no_lineno)

    if stats:
        counts = count_by_level(filtered)
        print_summary(filtered, counts, total)
