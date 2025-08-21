class LLMProvider:
    def summarize(self, prompt: str, timeout: float = 8.0) -> str:
        raise NotImplementedError
