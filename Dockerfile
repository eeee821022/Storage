使用 Python 3.11 的輕量級映像
FROM python:3.11-slim

設定工作目錄
WORKDIR /app

安裝 FFmpeg (yt-dlp 轉換 MP3 所需的外部工具)
在 Debian/Ubuntu (slim image based on debian) 上，使用 apt-get 安裝
這是確保 ffmpeg 可用的最簡單方式
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

複製 Python 依賴檔案
COPY requirements.txt .

安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

複製應用程式程式碼 (backend_server.py)
COPY backend_server.py .

由於我們使用絕對路徑，請將 FFmpeg 路徑改回系統預設，讓 Docker 容器可以找到
警告：此處 FFMPEG_PATH 和 YTDLP_PATH 在容器內使用預設值
ENV FFMPEG_PATH="ffmpeg"
ENV YTDLP_PATH="yt-dlp"

暴露 Port 5000 (但通常雲端服務會使用 $PORT 環境變數)
EXPOSE 5000

啟動應用程式
程式會監聽 0.0.0.0 讓外部可以存取
CMD ["python", "backend_server.py"]