from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from .levels import Level, LEVEL_STYLE
from .parser import LogLine

console = Console(highlight=False)

def _level_badge(lvl: Level) -> Text:
    label, style = LEVEL_STYLE[lvl]
    t = Text()
    t.append(f" {label} ", style=f"bold {style} on grey19")
    return t

def print_lines(lines: list[LogLine], *, show_lineno: bool = True, context_size: int = 0) -> None:
    for line in lines:
        row = Text()
        if show_lineno:
            row.append(f"{line.lineno:>6}  ", style="grey42")
        row.append_text(_level_badge(line.level))
        row.append("  ")
        row.append(line.message, style="white")
        console.print(row, highlight=False)

def print_summary(lines: list[LogLine], counts: dict[Level, int], total_input: int) -> None:
    table = Table(box=None, padding=(0, 2, 0, 0), show_header=False)
    table.add_column(style="grey50")
    table.add_column(justify="right")
    table.add_column()

    for lvl in sorted(counts, reverse=True):
        label, style = LEVEL_STYLE[lvl]
        bar_len = int(counts[lvl] / max(total_input, 1) * 40)
        bar = "█" * bar_len
        table.add_row(label, str(counts[lvl]), Text(bar, style=style))

    console.print()
    console.print(Panel(
        table,
        title=f"[grey50]{len(lines)} of {total_input} lines[/grey50]",
        border_style="grey23",
        expand=False,
    ))

def print_fields(lines: list[LogLine]) -> None:
    all_fields: dict[str, set] = {}
    for l in lines:
        for k, v in l.fields.items():
            all_fields.setdefault(k, set()).add(v)

    if not all_fields:
        console.print("[grey50]no key=value fields found[/grey50]")
        return

    table = Table(box=None, padding=(0, 2, 0, 0), show_header=True, header_style="grey50")
    table.add_column("field")
    table.add_column("unique values", style="grey70")
    for k, vals in sorted(all_fields.items()):
        sample = ", ".join(sorted(vals)[:5])
        if len(vals) > 5:
            sample += f" … +{len(vals)-5}"
        table.add_row(k, sample)

    console.print(table)
