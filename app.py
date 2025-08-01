from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from google.cloud import texttospeech
from dotenv import load_dotenv
import os
import uuid

# 환경 변수에서 키 불러오기
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

tts_client = texttospeech.TextToSpeechClient()

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