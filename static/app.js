// 取得彈出視窗相關的元素
const modal = document.getElementById('details-modal');
const modalBg = document.getElementById('modal-bg');
const modalCloseBtn = document.getElementById('modal-close-btn');
const modalOkBtn = document.getElementById('modal-ok-btn');
const modalContent = document.getElementById('modal-content');
const modalTitle = document.getElementById('modal-title');

// 關閉視窗的事件綁定
function closeModal() { modal.classList.remove('is-active'); }
modalBg.addEventListener('click', closeModal);
modalCloseBtn.addEventListener('click', closeModal);
modalOkBtn.addEventListener('click', closeModal);

// 🌟 新增功能：根據 ID (slug) 取得詳細資料並打開視窗
window.fetchDetails = function(slug) {
    // 1. 先打開視窗，並顯示載入中
    modal.classList.add('is-active');
    modalTitle.innerText = "正在取得動畫資料...";
    modalContent.innerHTML = '<p class="has-text-centered has-text-grey">📡 正在連線...</p>';

    // 2. 呼叫我們後端的公開詳細資料 API
    fetch(`/api/details/${slug}`)
        .then(response => {
            if (!response.ok) throw new Error("取得資料失敗");
            return response.json();
        })
        .then(data => {
            const info = data.data;
            modalTitle.innerText = info.title;
            
            // 處理標籤陣列
            const genresTags = info.genres.map(g => `<span class="tag is-primary is-light">${g}</span>`).join(' ');
            const mainTags = info.main_tags.map(t => `<span class="tag is-danger is-light">${t}</span>`).join(' ');
            const altTitlesList = info.alt_titles.map(title => `<li>${title}</li>`).join('');

            // 動態生成 HTML 內容 (加入新欄位並優化排版)
            modalContent.innerHTML = `
                <div class="content is-medium">
                    <p>
                        <strong>📅 播出時間：</strong> ${info.season_year} 
                        &nbsp;&nbsp;&nbsp; 
                        <strong>📺 狀態：</strong> <span class="tag is-info is-light">${info.status}</span>
                    </p>
                    
                    <p>
                        <strong>⭐ 觀眾評分：</strong> <strong class="has-text-warning-dark">${info.score}</strong> 
                        &nbsp;&nbsp;&nbsp; 
                        <strong>📼 總集數：</strong> ${info.episodes}
                    </p>
                    
                    <p><strong>🏢 製作公司：</strong> ${info.studio}</p>
                </div>
                
                <p><strong>🏷️ 動畫類型 (Genre)：</strong></p>
                <div class="tags">${genresTags}</div>
                
                ${info.main_tags.length > 0 ? `
                    <p><strong>📌 主要標籤 (Main tags)：</strong></p>
                    <div class="tags">${mainTags}</div>
                ` : ''}

                ${info.alt_titles.length > 0 ? `
                    <p><strong>📝 其他譯名 (Alternative titles)：</strong></p>
                    <div class="content">
                        <ul>${altTitlesList}</ul>
                    </div>
                ` : ''}
            `;
        })
};

// ==========================================
// 下面是原本的搜尋功能，只有修改了按鈕的 onclick
// ==========================================
// [UX 優化] 監聽搜尋輸入框的鍵盤事件
document.getElementById('search-keyword').addEventListener('keypress', function(event) {
    // 判斷按下的鍵是不是 Enter (鍵盤代碼為 'Enter')
    if (event.key === 'Enter') {
        // 阻止預設行為（防止表單送出重新整理網頁）
        event.preventDefault();
        // 模擬使用者用滑鼠點擊了「搜尋按鈕」
        document.getElementById('search-btn').click();
    }
});

document.getElementById('search-btn').addEventListener('click', function() {
    const keyword = document.getElementById('search-keyword').value;
    const resultsContainer = document.getElementById('search-results');
    
    if (!keyword) return alert("請先輸入關鍵字！");
    resultsContainer.innerHTML = '<div class="column has-text-centered has-text-grey-light">(正在查詢相關動畫...)</div>';

    fetch(`/api/search?keyword=${encodeURIComponent(keyword)}`)
        .then(response => {
            if (!response.ok) throw new Error("❌ 代理伺服器內部錯誤，請稍後再試。");
            return response.json();
        })
        .then(data => {
            resultsContainer.innerHTML = '';
            if (!data.results || data.results.length === 0) {
                resultsContainer.innerHTML = '<div class="column has-text-centered has-text-danger">❓ 找不到可能的動畫結果，試試中/英文別名。</div>';
                return;
            }

            data.results.forEach(anime => {
                const animeCardHTML = `
                    <div class="column is-one-third-desktop is-half-tablet">
                        <div class="card">
                            <div class="card-image">
                                <figure class="image is-4by3">
                                    <img src="${anime.cover_image || 'https://via.placeholder.com/400x300'}" alt="${anime.title}" style="object-fit: cover;">
                                </figure>
                            </div>
                            <div class="card-content">
                                <div class="media">
                                    <div class="media-content">
                                        <p class="title is-5">${anime.title}</p>
                                        <p class="subtitle is-6">年份: ${anime.year}</p>
                                    </div>
                                </div>
                                <div class="content has-text-centered">
                                    <button class="button is-info is-small is-outlined is-fullwidth" onclick="fetchDetails('${anime.slug}')">
                                        📖 查看詳細資料
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                resultsContainer.insertAdjacentHTML('beforeend', animeCardHTML);
            });
        })
        .catch(error => {
            resultsContainer.innerHTML = `<div class="column has-text-centered has-text-danger">${error.message}</div>`;
        });
});