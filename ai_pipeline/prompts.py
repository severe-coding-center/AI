def build_prompt(text: str, max_chars: int = 80) -> str:
    rules = f"""
- 1~2문장, {max_chars}자 내외.
- 행동 지침만 유지. 기관명/기호/중복 제거.
- "~하시기 바랍니다" 대신 "~하시면 좋습니다" 같은 친절한 말투.
- 새로운 정보 추가 금지. 수치/시간 보존.
- 출력은 반드시 JSON 한 줄: {{"summary":"<string>"}}
""".strip()
    return f"다음 안내문을 위 규칙대로 요약하세요.\n규칙:\n{rules}\n\nInput:\n{text}"
