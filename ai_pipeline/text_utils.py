import re

ORG = re.compile(r"\[[^\]]+\]")          # [기관명] 제거
BUL = re.compile(r"[△•\-▪️·]+")          # 불릿 → 쉼표
SPC = re.compile(r"\s+")

def normalize(t: str) -> str:
    t = ORG.sub(" ", t)
    t = BUL.sub(", ", t)
    t = t.replace("야외할동", "야외활동")
    return SPC.sub(" ", t).strip()

def polite(t: str) -> str:
    return (t.replace("주시기 바랍니다", "주시면 좋습니다")
             .replace("하시기 바랍니다", "하시면 좋습니다")
             .replace("유의하시기 바랍니다", "유의해 주시면 좋습니다"))

def clamp(t: str, n: int) -> str:
    return t if len(t) <= n else t[:n].rstrip(" ,.;:·-") + "…"
