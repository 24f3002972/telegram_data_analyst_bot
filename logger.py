import json
import os
import re
from datetime import datetime
 
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "run.jsonl")
 
# Patterns that catch common secret formats: KEY=value / TOKEN=value pairs,
# Telegram bot tokens (digits:AA...), and common provider key prefixes.
_SECRET_PATTERNS = [
    re.compile(r"([A-Za-z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)[A-Za-z0-9_]*\s*[:=]\s*)\S+", re.IGNORECASE),
    re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{30,}\b"),          # Telegram bot token shape
    re.compile(r"\bgsk_[A-Za-z0-9]{20,}\b"),                  # Groq keys
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),                   # OpenAI-style keys
    re.compile(r"\btvly-[A-Za-z0-9-]{10,}\b"),                # Tavily keys
]
 
 
def _redact(value):
    """Recursively redact secret-looking substrings from strings, dicts, and lists."""
    if isinstance(value, str):
        redacted = value
        for pattern in _SECRET_PATTERNS:
            if pattern.groups:
                redacted = pattern.sub(lambda m: m.group(1) + "[REDACTED]", redacted)
            else:
                redacted = pattern.sub("[REDACTED]", redacted)
        return redacted
    if isinstance(value, dict):
        return {k: _redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact(v) for v in value]
    return value
 
 
def log_event(step, data):
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "step": step,
        "data": _redact(data),
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
