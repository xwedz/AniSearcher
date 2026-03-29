# 🎌 AniSearcher - 動漫資訊雙引擎代理系統

[![Deploy Status](https://img.shields.io/badge/Deploy-Render-success?style=for-the-badge&logo=render)](你的Render網址)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00a393?style=for-the-badge&logo=fastapi)]()

這是一個基於 **FastAPI** 打造的現代化微服務 API 代理 (Proxy) 與資料聚合系統。本專案採用 **BFF (Backend For Frontend)** 架構，旨在解決跨語系動漫資訊檢索的痛點，並實作了高可用性的第三方 API 容錯與備援機制。

線上使用: https://anisearcher.onrender.com

---

## ✨ 核心系統特色與架構亮點

### 1. 雙引擎資料聚合 (Dual-Engine Data Aggregation)
* **痛點：** 前端使用者習慣輸入繁體中文，但國際主流的開源 ACG 資料庫 (如 MyAnimeList/Jikan) 僅支援英文或羅馬拼音的精準檢索。
* **解決方案：** 實作中介軟體 (Middleware) 進行資料過濾與轉換。系統首先請求 **Bangumi API**，利用其強大的中文社群資料庫取得目標動畫的日文原名或羅馬拼音別名。
* **繁簡防呆：** 整合 `zhconv` 套件，在請求 Bangumi 前自動處理繁簡體編碼差異，確保高命中率。

### 2. 備援重試機制 (Fallback & Retry System)
為了應對外部 API 可能的連線失敗或空值回傳，後端引擎會自動從 Bangumi 的 JSON 回應中解析出一個「可能名稱清單 (Candidate List)」。系統會依次使用清單中的名稱向 **Jikan API (MyAnimeList)** 進行重試，直到成功獲取完整資訊為止，大幅提升了系統的容錯率 (Fault Tolerance)。

### 3. BFF 架構與合規性 (BFF Architecture & Compliance)
* **資料解耦：** 採用 Backend For Frontend 模式。後端負責複雜的資料庫請求、限速保護 (Rate Limiting) 以及巢狀 JSON 的重組與翻譯 (如：將英文的播出狀態與季節在地化為中文)。
* **API 合規：** 系統底層資料源完全遵循服務條款 (ToS)，使用官方開源的 Jikan API v4，確保正式上線的合法性與穩定性。前端僅接收處理完畢的乾淨 JSON，達到完美的前後端分離。

### 4. CI/CD 與雲端原生部署 (Cloud-Native Deployment)
* **版本控制與隔離：** 使用 Git 進行版本控制，並透過 `.gitignore` 嚴格隔離本地虛擬環境 (`.venv`) 與系統日誌，確保程式碼庫的純淨。
* **自動化上線：** 專案已與 GitHub 整合，並成功部署至 **Render** 雲端平台 (PaaS)。配置了專屬的 `requirements.txt` (包含 `uvicorn[standard]` 等底層依賴) 與啟動指令，實現全自動化建置與 HTTPS 安全憑證核發。

---

## 🛠️ 技術棧 (Tech Stack)

* **後端框架：** Python 3, FastAPI, Uvicorn
* **前端介面：** HTML5, CSS3, Vanilla JavaScript (Fetch API)
* **資料處理：** Requests, zhconv, urllib
* **部署與維運：** Git, GitHub, Render (PaaS)
* **串接 API：** Bangumi API, Jikan API v4 (MyAnimeList)

---

## 🚀 本地端運行指南 (Local Setup)

如果您希望在本地環境運行本系統，請依照以下步驟操作：

1. **複製專案庫**
   \`\`\`bash
   git clone https://github.com/xwedz/AniSearcher.git
   cd AniSearcher
   \`\`\`

2. **建立並啟動虛擬環境 (強烈建議)**
   \`\`\`bash
   # Windows
   python -m venv .venv
   .venv\\Scripts\\activate
   \`\`\`

3. **安裝相依套件**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **啟動伺服器**
   \`\`\`bash
   uvicorn portfolio_api:app --host 127.0.0.1 --port 8000 --reload
   \`\`\`

5. **開啟瀏覽器**
   前往 \`http://127.0.0.1:8000\` 即可開始使用。

---

