import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .levels import Level, detect

_TS_PATTERNS = [
    re.compile(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)'),
    re.compile(r'(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2})'),
    re.compile(r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})'),
]

@dataclass
class LogLine:
    raw:       str
    lineno:    int
    level:     Level
    timestamp: Optional[str] = None
    message:   str = ""
    fields:    dict = field(default_factory=dict)

def _extract_ts(line: str) -> Optional[str]:
    for pat in _TS_PATTERNS:
        m = pat.search(line)
        if m:
            return m.group(1)
    return None

def _extract_kv(line: str) -> dict:
    return {m.group(1): m.group(2) for m in re.finditer(r'(\w+)=("(?:[^"\\]|\\.)*"|\S+)', line)}

def parse_line(raw: str, lineno: int) -> LogLine:
    ts  = _extract_ts(raw)
    kv  = _extract_kv(raw)
    lvl = detect(raw)
    msg = raw.strip()
    return LogLine(raw=raw, lineno=lineno, level=lvl, timestamp=ts, message=msg, fields=kv)

def parse_stream(lines) -> list[LogLine]:
    return [parse_line(line.rstrip('\n'), i + 1) for i, line in enumerate(lines)]
