import easyocr
from gtts import gTTS
import tempfile, os, time
from playsound import playsound
import numpy as np
from typing import Any, List
import re

def _normalize_text(s: str) -> str:
    """OCR 결과 문자열을 공백 정리해서 깔끔하게 반환"""
    return re.sub(r"\s+", " ", s).strip()

class OCRTTSModule:
    def __init__(self, lang=('ko','en'), min_interval=1.5):
        """
        lang: OCR 언어 (tuple)
        min_interval: 같은 글자를 반복해서 읽지 않도록 제한 시간(초)
        """
        self.reader = easyocr.Reader(list(lang), gpu=False)
        self.last_text = ""
        self.last_time = 0
        self.min_interval = min_interval

    def process_frame(self, frame: np.ndarray) -> str:
        raw: List[Any] = self.reader.readtext(frame, detail=0, paragraph=True)

        texts: List[str] = []
        if raw and isinstance(raw[0], str):
            texts = [t for t in raw if isinstance(t, str)]
        else:
            texts = [
                item[1] for item in raw
                if isinstance(item, (list, tuple)) and len(item) >= 2 and isinstance(item[1], str)
            ]

        text = _normalize_text(" ".join(texts))
        now = time.time()

        if text and (text != self.last_text or now - self.last_time > self.min_interval):
            print("[OCR]", text)
            self.speak(text)
            self.last_text = text
            self.last_time = now

        return text

    def speak(self, text: str):
        """텍스트를 음성으로 읽기"""
        tts = gTTS(text=text, lang='ko')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            fname = fp.name
            tts.save(fname)
        playsound(fname)
        os.remove(fname)
