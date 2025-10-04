from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi import UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from google.cloud import texttospeech
from dotenv import load_dotenv
import os
import uuid
from pathlib import Path

# === (추가) OCR에 필요한 모듈 ===
import numpy as np
import cv2
import tempfile
import easyocr

# 환경 변수에서 키 불러오기
load_dotenv()
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path:
    raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS 환경변수가 필요합니다.")
if not Path(cred_path).exists():
    raise FileNotFoundError(f"서비스 키 파일이 없습니다: {cred_path}")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
tts_client = texttospeech.TextToSpeechClient()

# === (추가) EasyOCR 리더 전역 초기화: 한글/영문 기본 ===
OCR_LANGS = os.getenv("OCR_LANGS", "ko,en").split(",")
ocr_reader = easyocr.Reader(OCR_LANGS, gpu=False)

# FastAPI 인스턴스 생성
app = FastAPI()

@app.post("/tts")
async def generate_tts(text: str = Form(...), speed: float = Form(1.0)):
    # 고유한 파일명 생성
    filename = f"output_{uuid.uuid4().hex[:8]}.mp3"

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.2
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)

    return FileResponse(path=filename, filename="output.mp3", media_type="audio/mpeg")

# === (추가) 이미지 → OCR → TTS(mp3) ===
@app.post("/ocr-read")
async def ocr_read(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    speed: float = Form(1.0),
):

    # 파일 확장자 확인
     # content_type 안전 체크
    ct = image.content_type or ""
    if not ct.startswith("image/"):
        raise HTTPException(status_code=415, detail="image/* 형식의 파일을 업로드하세요.")

    # 바이트 읽고 OpenCV 이미지로 변환
    data = await image.read()
    npbuf = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npbuf, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="이미지 디코딩 실패")

    # OCR 수행
    # detail=0 → 문자열 리스트, paragraph=True → 문단 묶기
    from typing import List, cast
    raw: List[str] = cast(List[str], ocr_reader.readtext(frame, detail=0, paragraph=True))
    texts = [s.strip() for s in raw if s and isinstance(s, str)]
    text = " ".join(texts)
    
    if not text:
        return JSONResponse(status_code=204, content={"detail": "no text detected"})
    
    # TTS 합성 (기존 클라이언트 재사용)
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=float(speed) if speed else 1.0
    )
    resp = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 임시파일로 보내되, 응답 후 삭제
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(resp.audio_content)
    tmp.flush()
    tmp.close()

    # 응답 완료 후 파일 삭제
    background_tasks.add_task(lambda p=tmp.name: os.path.exists(p) and os.remove(p))
    return FileResponse(
        path=tmp.name,
        filename="ocr_tts.mp3",
        media_type="audio/mpeg"
    )