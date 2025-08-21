import os
import google.generativeai as genai

# API 키 읽기
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY 환경변수를 설정하세요!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = """
다음 안내문을 친절한 말투로 1~2문장, 80자 이내로 요약하세요.
출력은 반드시 JSON 한 줄: {"summary":"..."} 만.

Input:
폭염 대비 안전관리 유의 △한낮 야외활동 자제 △충분한 수분 섭취
△야외활동 시 그늘에서 휴식을 취하는 등 건강관리에 유의하시기 바랍니다.[성주군]
"""

response = model.generate_content(prompt)
print("LLM Output:", response.text)
