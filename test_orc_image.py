import cv2
from orc_tts import OCRTTSModule   # 파일명이 ocr_tts.py면 from ocr_tts import ...

# 테스트 이미지 경로 (한글/영문 텍스트가 있는 사진)
IMG = r"E:\2025\test.png"

mod = OCRTTSModule()

# TTS 소음 싫으면 주석 해제: 말하기 함수 무력화
# mod.speak = lambda text: print(f"[TTS] {text}")

img = cv2.imread(IMG)
if img is None:
    raise SystemExit(f"이미지를 못 읽었습니다: {IMG}")

text = mod.process_frame(img)
print("[RESULT]", text)

cv2.imshow("image", img)
cv2.waitKey(1500)  # 1.5초 보여주고
cv2.destroyAllWindows()