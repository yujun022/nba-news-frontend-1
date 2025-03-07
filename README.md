# nba-news-frontend

1. 設定說明

本專案包含一個爬取 https://tw-nba.udn.com/nba/index 焦點新聞的爬蟲，以及一個提供 API 供前端使用的後端服務。

1.1 環境需求

Python 3.9+

MySQL 8.0+

Node.js 16+

瀏覽器 (測試前端使用)

1.2 安裝步驟

Clone 本專案

git clone https://github.com/yujun022/nba-news-frontend.git

cd nba-news-frontend

建立 Python 虛擬環境

python -m venv venv

source venv/bin/activate  # Windows 使用 venv\Scripts\activate

安裝後端依賴套件

pip install -r requirements.txt

設定 MySQL 資料庫

mysql -u root -p

CREATE DATABASE nba_news;

設定環境變數 (.env)

cp .env.example .env

# 編輯 .env，填寫資料庫設定
