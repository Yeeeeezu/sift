import re
from typing import Optional
from .levels import Level
from .parser import LogLine

def apply_filters(
    lines: list[LogLine],
    *,
    min_level: Optional[Level] = None,
    grep: Optional[str] = None,
    ignore: Optional[str] = None,
    field_filter: Optional[dict] = None,
) -> list[LogLine]:
    out = lines

    if min_level is not None:
        out = [l for l in out if l.level >= min_level]

    if grep:
        pat = re.compile(grep, re.IGNORECASE)
        out = [l for l in out if pat.search(l.raw)]

    if ignore:
        pat = re.compile(ignore, re.IGNORECASE)
        out = [l for l in out if not pat.search(l.raw)]

    if field_filter:
        for key, val in field_filter.items():
            out = [l for l in out if l.fields.get(key) == val or
                   l.fields.get(key) == f'"{val}"']

    return out

def count_by_level(lines: list[LogLine]) -> dict[Level, int]:
    counts: dict[Level, int] = {}
    for l in lines:
        counts[l.level] = counts.get(l.level, 0) + 1
    return counts
