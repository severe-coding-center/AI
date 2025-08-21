import os, sys, json, traceback
import google.generativeai as genai

def safe_print(title, value):
    print(f"[DBG] {title}: {value}")

def main():
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        safe_print("PYTHON", sys.version)
        safe_print("CWD", os.getcwd())
        safe_print("HAS_KEY", bool(api_key))
        if api_key:
            safe_print("KEY_TAIL", api_key[-6:])  # 마지막 몇 글자만
        else:
            print("[ERR] GOOGLE_API_KEY 환경변수가 없습니다. `export GOOGLE_API_KEY=...` 후 터미널 새로 열고 다시 실행하세요.")
            return

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = """
다음 안내문을 친절한 말투로 1~2문장, 80자 이내로 요약하세요.
출력은 반드시 JSON 한 줄: {"summary":"..."} 만.

Input:
폭염 대비 안전관리 유의 △한낮 야외활동 자제 △충분한 수분 섭취
△야외활동 시 그늘에서 휴식을 취하는 등 건강관리에 유의하시기 바랍니다.[성주군]
""".strip()

        safe_print("CALLING_MODEL", "generate_content")
        resp = model.generate_content(prompt)
        # 원시 응답 덤프
        try:
            print("[RAW]", resp)
        except Exception:
            pass

        # 공통적으로 text 속성 시도
        text = getattr(resp, "text", None)
        safe_print("RESP.text is None?", text is None)

        # candidates 경로로도 시도
        cand_text = None
        try:
            if hasattr(resp, "candidates") and resp.candidates:
                parts = getattr(resp.candidates[0].content, "parts", None)
                if parts and len(parts) and hasattr(parts[0], "text"):
                    cand_text = parts[0].text
        except Exception:
            traceback.print_exc()

        out = text or cand_text
        if not out:
            # 안전성 필터에 막힌 경우 안내
            fb = getattr(resp, "prompt_feedback", None)
            if fb:
                print("[WARN] 빈 응답. prompt_feedback:", fb)
            else:
                print("[WARN] 빈 응답을 받았습니다.")
            return

        print("\n=== LLM Output ===")
        print(out)

    except Exception as e:
        print("[EXC]", type(e).__name__, "-", e)
        traceback.print_exc()

if __name__ == "__main__":
    main()
