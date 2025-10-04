FROM python:3.11-slim

WORKDIR /app

# 먼저 requirements만 복사해서 캐시 최적화
COPY requirements.txt .

# 혹시 모를 일반 opencv 제거 후 headless 설치를 보장
RUN pip install --no-cache-dir -r requirements.txt \
 && pip uninstall -y opencv-python opencv-contrib-python 2>/dev/null || true \
 && pip install --no-cache-dir opencv-python-headless==4.10.0.84

# 앱 소스 복사
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
