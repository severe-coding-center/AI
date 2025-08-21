import os
from ai_pipeline import Summarizer

# 환경변수: OPENAI_API_KEY 필수
os.environ.setdefault("LLM_MODEL", "gpt-4o-mini")

txt = "폭염 대비 안전관리 유의 △한낮 야외활동 자제 △충분한 수분 섭취 △야외활동 시 그늘에서 휴식을 취하는 등 건강관리에 유의하시기 바랍니다.[성주군]"

summ = Summarizer()
summary, ssml = summ.summarize_to_ssml(txt)

print("요약:", summary)
print("SSML:", ssml)
