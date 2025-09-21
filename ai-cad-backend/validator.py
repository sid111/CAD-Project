# validator.py
import re

ALLOWED_PRIMITIVES = ["cube", "sphere", "cylinder", "difference", "union", "translate", "rotate"]
BLACKLIST = ["import ", "open(", "exec(", "subprocess", "os.", "sys.", "eval(", "`", "$("]

def is_safe(code: str) -> bool:
    """Basic safety + validity checks"""
    low = code.lower()

    # Blacklist dangerous tokens
    for bad in BLACKLIST:
        if bad in low:
            return False

    # Must contain at least one allowed primitive
    if not any(re.search(r"\b" + p + r"\b", low) for p in ALLOWED_PRIMITIVES):
        return False

    # Check braces and parens
    if code.count("{") != code.count("}"):
        return False
    if code.count("(") != code.count(")"):
        return False

    # Length guard
    if len(code) > 8000:
        return False

    return True
