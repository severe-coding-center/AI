import re
from .text_utils import clamp, polite

def extractive_fallback(text: str, max_chars: int = 80) -> str:
    clauses = re.split(r"[,.·;:]", text)
    verbs = ["자제", "피하", "섭취", "휴식", "유의", "주의", "대비", "신고", "대피"]
    candidates = [c.strip() for c in clauses if c.strip()
                  and any(v in c for v in verbs)]
    if not candidates:
        candidates = [c.strip() for c in clauses if c.strip()]
    s = " ".join(candidates[:2]) if candidates else text
    s = clamp(s, max_chars)
    if not s.endswith(("요", "다", ".", "!", "?")):
        s += "."
    return polite(s)
