# 使用 Python 3.11 作為基礎映像
FROM python:3.11

# 設定工作目錄
WORKDIR /app

RUN pip install aiomysql

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 wait-for-it 腳本，用於等待資料庫服務啟動
RUN apt-get update && apt-get install -y curl \
    && curl -L https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it \
    && chmod +x /usr/local/bin/wait-for-it

# 複製所有程式碼到容器內
COPY . .

# 指定啟動指令，首先使用 wait-for-it 等待 MySQL 資料庫服務啟動
CMD ["wait-for-it", "nba_mysql:3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
