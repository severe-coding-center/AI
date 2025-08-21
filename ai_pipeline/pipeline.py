import json, re
from .config import MAX_CHARS, TIMEOUT
from .text_utils import normalize, clamp, polite
from .ssml import to_ssml
from .prompts import build_prompt
from .fallback import extractive_fallback
from .providers import OpenAIProvider, LLMProvider

JSON_SUM_RE = re.compile(r'\{[^{}]*"summary"\s*:\s*"(.+?)"[^{}]*\}', re.S)

def parse_summary_json(s: str) -> str:
    s = re.sub(r"```(?:json)?\s*|\s*```", "", s).strip()
    m = JSON_SUM_RE.search(s)
    if m: return m.group(1).strip()
    try:
        data = json.loads(s)
        if isinstance(data, dict) and "summary" in data:
            return str(data["summary"]).strip()
    except Exception:
        pass
    raise ValueError("Malformed JSON from LLM")

class Summarizer:
    def __init__(self, provider: LLMProvider | None = None, max_chars: int = MAX_CHARS):
        self.provider = provider or OpenAIProvider()
        self.max_chars = max_chars

    def summarize(self, text: str) -> dict:
        clean = normalize(text)
        prompt = build_prompt(clean, self.max_chars)
        try:
            raw = self.provider.summarize(prompt)
            summary = parse_summary_json(raw)
        except Exception:
            summary = extractive_fallback(clean, self.max_chars)

        summary = polite(summary.strip())
        summary = clamp(summary, self.max_chars)
        if not summary.endswith(("요", "다", ".", "!", "?")):
            summary += "."
        return {"summary": summary}

    def summarize_to_ssml(self, text: str, pause_ms: int = 300) -> tuple[str, str]:
        out = self.summarize(text)
        s = out["summary"]
        return s, to_ssml(s, pause_ms=pause_ms)
