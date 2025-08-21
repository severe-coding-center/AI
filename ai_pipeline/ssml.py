import re
def to_ssml(t: str, pause_ms: int = 300) -> str:
    sents = [s for s in re.split(r"(?<=[\.!?]|요|다)\s+", t) if s]
    return "<speak>" + f'<break time="{pause_ms}ms"/>'.join(sents) + "</speak>"
