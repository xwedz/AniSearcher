# AniSearcher
[![Deploy Status](https://img.shields.io/badge/Deploy-Render-success?style=for-the-badge&logo=render)](https://anisearcher.onrender.com)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00a393?style=for-the-badge&logo=fastapi)]()

AniSearcher 讓你可以利用繁體中文，方便快速的搜尋到各種動畫(及相關作品)的資料，馬上試著用AniSearcher搜索各種動畫資料吧 ! 

線上使用: https://anisearcher.onrender.com

## 🌟 Features

* **中文友善搜尋：** 整合 Bangumi API 取得日文原名與羅馬拼音，再向外檢索，大幅提高中文關鍵字的命中率。
* **BFF 代理架構：** 後端負責處理外部 API 的 Rate Limit 與巢狀資料重組，前端只需接收乾淨的 JSON。
* **高可用性備援：** 若首選名稱搜尋失敗，系統會自動從候選名單中進行重試，降低空值回傳率。

## 🛠️ Tech Stack

* **Backend:** Python 3, FastAPI, Uvicorn
* **Frontend:** HTML5, CSS3, Vanilla JS
* **External APIs:** Bangumi API, Tenrai API (MyAnimeList Data)

## 🚀 Local Setup

1. Clone 專案並建立虛擬環境：  
   `git clone https://github.com/xwedz/AniSearcher.git`  
   `cd AniSearcher`  
   `python -m venv .venv`  
   `.venv\Scripts\activate`
2. 安裝套件：
   `pip install -r requirements.txt`
3. 啟動伺服器：
   `uvicorn AniSearcherV2:app --host 127.0.0.1 --port 8000 --reload`
> 啟動後開啟瀏覽器前往 `http://127.0.0.1:8000` 即可使用。

## 📝 Changelog

* **2026-09-01**
  * `Fix`: 解決上游 Jikan API 進入 brownout 階段導致的 504 Gateway Timeout 錯誤。
  * `Refactor`: 將依賴之動漫資料源無痛遷移至 Tenrai API，恢復系統正常運作。