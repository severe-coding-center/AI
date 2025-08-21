import os
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MAX_CHARS = int(os.getenv("MAX_CHARS", "80"))
TIMEOUT = float(os.getenv("TIMEOUT", "8.0"))
