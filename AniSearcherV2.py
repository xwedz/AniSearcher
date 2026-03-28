from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
import urllib.parse
import time
import zhconv

app = FastAPI(title="Portfolio Anime Search (Jikan Edition)", description="符合 ToS 規範的動漫搜尋展示作品")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse('static/index.html')

# =====================================================================
# 🌟 [在地化字典] 保留之前的標籤翻譯查表
# =====================================================================
TAG_TRANSLATIONS = {
    # Genres (類型)
    "Action": "動作", "Adventure": "冒險", "Comedy": "喜劇", "Drama": "劇情",
    "Fantasy": "奇幻", "Romance": "戀愛", "Sci-Fi": "科幻", "Slice of Life": "日常",
    "Psychological": "心理", "Mystery": "懸疑", "Horror": "恐怖", "Sports": "運動",
    "Supernatural": "超自然","Award Winning": "得獎作品", "Ecchi": "色情",
    
    # Tags (標籤)
    "Tragedy": "悲劇", "Magic": "魔法", "School": "校園", "Time Manipulation": "穿越",
    "Philosophy": "哲學", "Coming of Age": "成長", "Male Protagonist": "男主角", 
    "Female Protagonist": "女主角", "Kuudere": "無口/三無", "Tsundere": "傲嬌",
    "Seinen": "青年", "Shounen": "少年", "Urban": "都市", "Full CGI": "全CG",
    "Demons": "惡魔", "Elf": "精靈", "Travel": "旅行", "Iyashikei": "治癒系",
    "Virtual World": "虛擬世界", "Video Game": "電玩遊戲", "Guns": "槍枝",
    "Battle Royale": "大逃殺", "Swordplay": "劍術", "Super Power": "超能力",
    "Ghost": "鬼魂", "Urban Fantasy": "都市幻想", "Environmental": "自然環境",
    "Idol": "偶像", "Revenge": "復仇", "Twins": "雙胞台", "Acting": "表演",
    "Family Life": "家庭日常", "Ensemble Cast": "群像戲", "Rural": "鄉村",
    "Primarily Teen Cast": "青少年主演", "Hikikomori": "蟄居族", "Gore": "血腥",
    "Zombie": "殭屍", "Survival": "生存", "Pandemic": "病毒爆發", 
    "School Club": "校園社團", "Detective": "偵探", "Anti-Hero": "反英雄",
    "Superhero": "超級英雄", "Parody": "戲仿", "Satire": "諷刺","Basketball": "籃球",
    "Volleyball": "排球", "Football": "足球", "Athletics": "陸上競技",
    "Primarily Male Cast": "男性主演", "Primarily Female Cast": "女性主演",
    "LGBTQ+ Themes": "LGBTQ+主題", "Yuri": "百合", "Cohabitation": "同居",
    "Age Gap": "年齡差", "Heterosexual": "異性戀", "Meta": "突破第四面牆",
    "Animals": "動物", "Slapstick": "鬧劇", "Surreal Comedy": "超現實喜劇",
    "Samurai": "武士", "Ninja": "忍者", "Orphan": "孤兒"
}

def translate_tags(tag_list):
    if not tag_list: return []
    translated_list = []
    for tag in tag_list:
        if tag in TAG_TRANSLATIONS:
            translated_list.append(f"{tag} ({TAG_TRANSLATIONS[tag]})")
        else:
            translated_list.append(tag)
    return translated_list

# =====================================================================
# 🌟 [輔助引擎] Bangumi 名稱彈藥庫 (保留強大的繁簡容錯機制)
# =====================================================================
def get_names_from_bangumi(keyword: str) -> list:
    simplified_keyword = zhconv.convert(keyword, 'zh-cn')
    search_url = f"https://api.bgm.tv/search/subject/{urllib.parse.quote(simplified_keyword)}"
    headers = {"User-Agent": "your_name/portfolio_project (https://github.com/your_username)"}
    params = {"type": 2, "responseGroup": "small"}
    possible_names = []
    
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=5)
        time.sleep(0.5) 
        if response.status_code == 200:
            data = response.json()
            if data.get("list") and len(data["list"]) > 0:
                best_match = data["list"][0]
                if best_match.get("name"):
                    possible_names.append(best_match["name"])
                
                subject_id = best_match.get("id")
                if subject_id:
                    detail_url = f"https://api.bgm.tv/v0/subjects/{subject_id}"
                    detail_res = requests.get(detail_url, headers=headers, timeout=5)
                    time.sleep(0.5)
                    if detail_res.status_code == 200:
                        detail_data = detail_res.json()
                        if "infobox" in detail_data:
                            for item in detail_data["infobox"]:
                                if item.get("key") == "别名" and isinstance(item.get("value"), list):
                                    for alias_obj in item["value"]:
                                        alias_text = alias_obj.get("v", "")
                                        if alias_text.isascii():
                                            possible_names.insert(0, alias_text)
        
        possible_names.append(keyword)
        unique_names = list(dict.fromkeys(possible_names))
        return unique_names
    except Exception:
        return [keyword]

# =====================================================================
# 🌟 [主架構] 搜尋功能 (改用 Jikan API，但維持相同的 JSON 輸出格式)
# =====================================================================
@app.get("/api/search")
def search_anime_public(keyword: str):
    name_candidates = get_names_from_bangumi(keyword)
    search_results = []
    
    for candidate_name in name_candidates:
        print(f"🔄 嘗試使用 '{candidate_name}' 搜尋 Jikan API...")
        safe_keyword = urllib.parse.quote(candidate_name)
        # 呼叫 Jikan v4 API
        target_url = f"https://api.jikan.moe/v4/anime?q={safe_keyword}&limit=6"
        
        try:
            response = requests.get(target_url, timeout=5)
            # 🌟 [重要] Jikan 有嚴格的 Rate Limit，必須 sleep 保護
            time.sleep(0.5) 
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data") and len(data["data"]) > 0:
                    print(f"✅ Jikan 命中！找到 {len(data['data'])} 筆結果。")
                    
                    for item in data["data"]:
                        # 🌟 [BFF 模式] 將 Jikan 的資料，包裝成前端原本認識的樣子
                        search_results.append({
                            "title": item.get("title", "未知"),      
                            # 將 Jikan 的 mal_id 偽裝成 slug 傳給前端
                            "slug": str(item.get("mal_id")),
                            "year": item.get("year", "未知") if item.get("year") else "未知",
                            "cover_image": item["images"]["jpg"]["large_image_url"] if "images" in item else ""
                        })
                    
                    return {"status": "success", "total_found": len(search_results), "results": search_results}
        except requests.exceptions.RequestException:
            continue
            
    return {"status": "success", "total_found": 0, "results": []}

# =====================================================================
# 🌟 [主架構] 詳細資料功能 (改用 Jikan API)
# =====================================================================
@app.get("/api/details/{slug}")
def get_anime_details_public(slug: str):
    
    # 這裡的 slug 其實是前面傳過來的 mal_id
    target_url = f"https://api.jikan.moe/v4/anime/{slug}"
    
    try:
        response = requests.get(target_url, timeout=5)
        time.sleep(0.5)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="❌ 無法從 Jikan 取得資料")
        
        item = response.json().get("data", {})
        if not item:
            raise HTTPException(status_code=404, detail="❓ 找不到資料")
            
# 解析 Jikan 獨特的資料結構
        studios = [s["name"] for s in item.get("studios", [])]
        studio_name = studios[0] if studios else "未知"
        
        genres = [g["name"] for g in item.get("genres", [])]
        themes = [t["name"] for t in item.get("themes", [])]
        alt_titles = [t["title"] for t in item.get("titles", []) if t.get("type") in ["Japanese", "Synonym"]]
        
        # 🌟 [新增] 解析季節與年份 (Season & Year)
        SEASON_MAP = {"spring": "春季", "summer": "夏季", "fall": "秋季", "winter": "冬季"}
        raw_season = item.get("season")
        raw_year = item.get("year")
        season_str = SEASON_MAP.get(raw_season, "") if raw_season else ""
        year_str = str(raw_year) if raw_year else "未知"
        season_year = f"{year_str} {season_str}".strip()

        # 🌟 [新增] 解析播出狀態 (Status)
        STATUS_MAP = {
            "Finished Airing": "已完結",
            "Currently Airing": "連載中",
            "Not yet aired": "未播出"
        }
        raw_status = item.get("status", "")
        status = STATUS_MAP.get(raw_status, raw_status)

        # 🌟 [新增] 解析評分 (Score) 與集數 (Episodes)
        score = item.get("score")
        score_str = f"{score} / 10" if score else "暫無評分"
        
        episodes = item.get("episodes")
        episodes_str = f"{episodes} 集" if episodes else "未知"

        # 🌟 [BFF 模式] 組裝成強化版的 clean_info 格式
        clean_info = {
            "title": item.get("title", "未知"),
            "season_year": season_year,  # 替換掉原本單純的 year
            "status": status,            # 新增
            "score": score_str,          # 新增
            "episodes": episodes_str,    # 新增
            "studio": studio_name,
            "genres": translate_tags(genres),
            "main_tags": translate_tags(themes),
            "alt_titles": alt_titles
        }
        
        return {"status": "success", "data": clean_info}

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="⚠️ 伺服器連線錯誤")

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["use_colors"] = False
    log_config["formatters"]["access"]["use_colors"] = False
    log_config["handlers"]["file"] = {
        "class": "logging.FileHandler",
        "filename": "portfolio_audit.log",
        "formatter": "default", 
    }
    log_config["loggers"]["uvicorn"]["handlers"].append("file")
    log_config["loggers"]["uvicorn.access"]["handlers"].append("file")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)