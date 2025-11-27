
# 使用官方 Python 映像檔
FROM python:3.10-slim

# 安裝 ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# 設定工作目錄
WORKDIR /app

# 複製檔案
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 同時啟動 Flask 和 Streamlit
CMD ["sh", "-c", "python proxy_server.py & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
