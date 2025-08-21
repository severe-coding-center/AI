import re
from openai import OpenAI
from ..config import OPENAI_API_KEY, LLM_MODEL, TIMEOUT
from .base import LLMProvider

SYS = 'You are a Korean public-safety summarizer. Output ONLY JSON: {"summary":"..."}'

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str | None = None, api_key: str | None = None):
        self.client = OpenAI(api_key=api_key or OPENAI_API_KEY)
        self.model = model or LLM_MODEL

    def summarize(self, prompt: str, timeout: float = TIMEOUT) -> str:
        resp = self.client.responses.create(
            model=self.model,
            input=[{"role":"system","content":SYS},
                   {"role":"user","content":prompt}],
            timeout=timeout,
        )
        txt = None
        for out in resp.output:
            if out.type == "message":
                for c in out.message.content:
                    if c.type == "text":
                        txt = c.text; break
        if not txt and hasattr(resp, "choices") and resp.choices:
            txt = resp.choices[0].message.get("content", "")
        if not txt:
            raise RuntimeError("OpenAI empty response")
        return txt
