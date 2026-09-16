import re
from enum import IntEnum

class Level(IntEnum):
    TRACE = 0
    DEBUG = 1
    INFO  = 2
    WARN  = 3
    ERROR = 4
    FATAL = 5

_PATTERNS = [
    (Level.FATAL, re.compile(r'\b(fatal|FATAL|crit|CRIT|critical|CRITICAL)\b')),
    (Level.ERROR, re.compile(r'\b(error|ERROR|err|ERR|exception|EXCEPTION|traceback|Traceback)\b')),
    (Level.WARN,  re.compile(r'\b(warn|WARN|warning|WARNING)\b')),
    (Level.DEBUG, re.compile(r'\b(debug|DEBUG|dbg|DBG)\b')),
    (Level.TRACE, re.compile(r'\b(trace|TRACE)\b')),
]

def detect(line: str) -> Level:
    for lvl, pat in _PATTERNS:
        if pat.search(line):
            return lvl
    return Level.INFO

LEVEL_STYLE = {
    Level.TRACE: ("TRACE", "grey50"),
    Level.DEBUG: ("DEBUG", "grey70"),
    Level.INFO:  ("INFO ",  "bright_cyan"),
    Level.WARN:  ("WARN ",  "yellow"),
    Level.ERROR: ("ERROR", "red"),
    Level.FATAL: ("FATAL", "bold red"),
}
