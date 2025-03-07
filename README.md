# nba-news-frontend

# 設定說明

## 1. 環境需求

-	Python 3.8+
-	MySQL 資料庫
-	Node.js (用於前端開發)
## 2 . 安裝依賴套件
```bash
pip install -r requirements.txt
```
## 3. 設定環境變數
請在專案根目錄建立 ```bash .env``` 檔案，內容如下：
```bash
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/nba_news
```
## 4. 運行專案
```uvicorn main:app --reload```







