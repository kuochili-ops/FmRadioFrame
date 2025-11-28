import streamlit as st
import base64
import json
import streamlit.components.v1 as components
import os

# 設定頁面
st.set_page_config(page_title="Radio & Weather Frame", layout="centered")

st.title("📻 智慧相框收音機 (修正新聞來源與速度)")
st.caption("新聞跑馬燈已變慢，並修正為更可靠的即時新聞來源。")

# ---------------- 1. Python 資料準備區 ----------------

# 檢查本地檔案並轉 Base64
def get_base64_image(path):
    """讀取本地檔案並轉為 Base64 字串"""
    mime_type = 'image/jpeg'
    if path.lower().endswith('.png'): mime_type = 'image/png'
    elif path.lower().endswith('.gif'): mime_type = 'image/gif'

    try:
        with open(path, "rb") as image_file:
            b64 = base64.b64encode(image_file.read()).decode()
            return f"data:{mime_type};base64,{b64}"
    except FileNotFoundError:
        return None

# 定義預設圖片路徑
default_image_paths = ["assets/photo1.jpg", "assets/photo2.jpg", "assets/photo3.jpg"] 

# 電台清單 (維持不變)
stations = [
    {"name": "ICRT (英語)", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台 (綜合)", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事 989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都 983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "https://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}, 
]

# 圖片處理
uploaded_files = st.file_uploader("📸 上傳相片", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

img_list = []
if uploaded_files:
    for file in uploaded_files:
        b64 = base64.b64encode(file.read()).decode()
        mime_type = file.type
        img_list.append(f"data:{mime_type};base64,{b64}")
else:
    # 使用本地 /assets/ 圖片作為預設
    for p in default_image_paths:
        b64_img = get_base64_image(p)
        if b64_img:
            img_list.append(b64_img)

    if not img_list:
        st.warning(f"⚠️ 在 /assets/ 中找不到預設圖片，請檢查路徑。")
        img_list = ["data:image/svg+xml;base64," + base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="562" viewBox="0 0 1000 562"><rect width="1000" height="562" fill="#555"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="60" fill="#fff">Upload Photos or Check /assets/</text></svg>').decode()]


# 轉 JSON 供 JS 使用
js_stations = json.dumps(stations)
js_images = json.dumps(img_list)
api_key = "dacfd5f7b7e6c05162ac1340b88b6cc0" 

# ---------------- 2. HTML/JS 前端核心 ----------------

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>

<style>
    body {{
        font-family: "Segoe UI", "Helvetica Neue", sans-serif;
        background-color: #0e1117;
        color: white;
        text-align: center;
        margin: 0;
        padding: 10px;
        box-sizing: border-box;
    }}
    /* --- 相框容器 --- */
    .frame-container {{
        width: 100%;
        max-width: 650px;
        margin: 0 auto 10px auto; 
        border: 4px solid #333;
        border-radius: 12px;
        background: #000;
        overflow: hidden;
        position: relative;
        aspect-ratio: 16/9;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }}

    /* --- 新聞跑馬燈 --- */
    .news-ticker-container {{
        max-width: 650px;
        margin: 0 auto 15px auto;
        background-color: #585d68; 
        color: #fff;
        padding: 5px 0;
        overflow: hidden; 
        white-space: nowrap; 
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}

    .news-ticker-content {{
        display: inline-block;
        padding-left: 100%; 
        font-weight: 500;
        font-size: 0.9em;
        /* >>> 跑馬燈速度修正：從 60s 增加到 90s <<< */
        animation: marquee 90s linear infinite; 
    }}

    /* 定義滾動動畫 */
    @keyframes marquee {{
        0% {{ transform: translateX(0%); }}
        100% {{ transform: translateX(-100%); }}
    }}

    /* --- 行動裝置優化 --- */
    @media (max-width: 700px) {{
        .controls {{ grid-template-columns: 1fr; gap: 10px; }}
        .card {{ padding: 10px; }}
        .card-title {{ display: none; }}
        .input-group {{ flex-direction: column; gap: 5px; }}
        audio {{ height: 30px; }}
        .weather-badge {{ bottom: 5px; right: 5px; padding: 4px 8px; font-size: 0.7rem; }}
        
        /* >>> 跑馬燈速度修正：從 90s 增加到 120s <<< */
        .news-ticker-content {{ animation: marquee 120s linear infinite; }}
    }}
    
    /* --- 其他樣式略... --- */
    .weather-badge {{ position: absolute; bottom: 15px; right: 15px; background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(4px); color: #fff; padding: 8px 15px; border-radius: 8px; z-index: 10; font-size: 0.9rem; }}
    .weather-row {{ display: flex; align-items: center; justify-content: flex-end; gap: 5px; }}
    .weather-temp {{ font-size: 1.4rem; font-weight: bold; color: #fab005; }}
    .weather-city {{ font-size: 0.85rem; font-weight: 600; margin-bottom: 2px; }}
    .weather-desc {{ font-size: 0.8rem; color: #ddd; }}
    .time-display {{ margin-top: 4px; font-size: 0.8rem; color: #ccc; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 4px; }}
    .frame-img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .controls {{ max-width: 650px; margin: auto; }}
    button {{ background-color: #ff4b4b; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; font-size: 14px; width: 100%; margin-top: 5px; transition: 0.2s; }}
    button.btn-blue {{ background-color: #1E90FF; }}
    button.btn-green {{ background-color: #32CD32; }}
    button.btn-gray {{ background-color: #555; margin-top:0; width: auto; font-size: 12px; }}
    input[type="text"] {{ width: 60%; padding: 6px; border-radius: 4px; border: 1px solid #555; background: #111; color: white; }}
    .input-group {{ display: flex; gap: 5px; margin-bottom: 10px; }}
    audio {{ width: 100%; height: 35px; margin-top: 8px; }}

</style>
</head>
<body>

    <div class="frame-container" id="frameBox">
        <img id="slideImg" class="frame-img" src="{img_list[0]}">
        
        <div class="weather-badge">
            <div class="weather-city" id="wd-city">Taipei, TW</div>
            <div class="weather-row">
                <img id="wd-icon" src="" style="width:35px; height:35px; display:none;">
                <span class="weather-temp" id="wd-temp">--°C</span>
            </div>
            <div class="weather-desc" id="wd-desc">Loading...</div>
            <div class="time-display" id="wd-time">--/-- --:--</div>
        </div>
    </div>

    <div class="news-ticker-container">
        <div class="news-ticker-content" id="newsTickerContent">新聞載入中...</div>
    </div>

    <div class="controls">
        <div class="card">
            <div class="card-title">🌦️ 城市 & 音樂</div>
            
            <div class="input-group">
                <input type="text" id="cityInput" value="Taipei, Taiwan" placeholder="Enter City">
                <button class="btn-gray" onclick="fetchWeather()">更新</button>
            </div>

            <span id="stationLabel" class="station-name">{stations[0]['name']}</span>
            <audio id="audioPlayer" controls></audio>
            
            <div style="display:flex; gap:5px; margin-top:5px;">
                <button class="btn-blue" onclick="prevStation()">⏮️</button>
                <button class="btn-blue" onclick="nextStation()">⏭️ 下一頻道</button>
            </div>
        </div>

        <div class="card">
            <div class="card-title">🖼️ 相框控制</div>
            <div style="margin-bottom:10px; font-size:0.85em; color:#aaa;">
                顯示：<span id="fitLabel">Cover (裁切)</span> | 比例：<span id="ratioLabel">16:9</span>
            </div>
            <button class="btn-green" onclick="toggleRatio()">📐 切換比例</button>
            <button onclick="toggleFit()">🔍 切換顯示</button>
        </div>
    </div>

    <script>
        // --- 設定新聞來源 (已更新為 Liberty Times) ---
        const NEWS_RSS_URL = 'https://news.ltn.com.tw/rss/all.xml'; // 自由時報即時新聞 (維持不變)
        const CORS_PROXY = 'https://api.allorigins.win/raw?url='; // CORS 代理服務 (更換回穩定服務)

        // JS 變數 (維持不變)
        const stations = {js_stations};
        const images = {js_images};
        const apiKey = "{api_key}";

        let currentStationIdx = 0;
        let currentImgIdx = 0;
        let currentRatio = "16/9";
        let currentFit = "cover";
        let hls = null; 

        // DOM 元素
        const audioPlayer = document.getElementById("audioPlayer");
        const stationLabel = document.getElementById("stationLabel");
        const slideImg = document.getElementById("slideImg");
        const frameBox = document.getElementById("frameBox");
        const newsTickerContent = document.getElementById("newsTickerContent");
        
        const wdCity = document.getElementById("wd-city");
        const wdTemp = document.getElementById("wd-temp");
        const wdDesc = document.getElementById("wd-desc");
        const wdIcon = document.getElementById("wd-icon");
        const wdTime = document.getElementById("wd-time");
        const cityInput = document.getElementById("cityInput");
        
        // --- 1. 即時新聞抓取與更新 (修正代理與解析) ---
        async function fetchLiveNews() {{
            const newsTickerElement = document.getElementById("newsTickerContent");
            newsTickerElement.innerText = "新聞載入中..."; // 確保使用正確的 DOM 元素

            try {{
                // 使用更可靠的 CORS 代理服務
                const response = await fetch(CORS_PROXY + encodeURIComponent(NEWS_RSS_URL));
                if (!response.ok) throw new Error(`Network response was not ok: ${{response.status}}`);
                
                const xmlText = await response.text();
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(xmlText, "text/xml");
                
                // 解析並提取 <item> 內的 <title>
                const items = xmlDoc.querySelectorAll('item');
                let headlines = [];
                
                items.forEach(item => {{
                    const titleElement = item.querySelector('title');
                    if (titleElement && titleElement.textContent) {{
                        const title = titleElement.textContent.trim();
                        // 排除標準的 RSS Feed 標題，避免標題重複
                        if (title.length > 5 && !title.includes("自由時報") && !title.includes("即時熱門新聞")) {{ 
                            headlines.push(title);
                        }}
                    }}
                }});

                if (headlines.length === 0) {{
                     newsTickerElement.innerText = "⭐ 即時新聞 ⭐ 資料為空或解析失敗，將在 10 分鐘後重試。";
                     return;
                }}

                // 組合並更新跑馬燈內容
                const separator = " ⭐ ⭐ ⭐ ";
                const newContent = separator + headlines.join(separator) + separator + separator + separator;

                // 為了確保 CSS 動畫能順利重啟，替換舊元素
                const container = newsTickerElement.parentElement;
                const oldTicker = document.getElementById("newsTickerContent");
                const newTicker = oldTicker.cloneNode(false); // 僅複製元素，不複製內容
                newTicker.innerText = newContent;
                
                // 移除舊元素，新增新元素
                oldTicker.remove();
                container.appendChild(newTicker);
                
            }} catch (error) {{
                console.error("新聞載入失敗:", error);
                newsTickerElement.innerText = `⭐ 即時新聞 ⭐ 載入失敗 (錯誤: ${{error.message}})，將在 10 分鐘後重試。`;
            }}
        }}


        // --- 2. 音樂播放邏輯 (HLS 支援, 維持不變) ---
        function playStation(index) {{
            const station = stations[index];
            stationLabel.innerText = station.name;
            const url = station.url;
            if (Hls.isSupported() && url.includes('.m3u8')) {{
                if (hls) {{ hls.destroy(); }}
                hls = new Hls();
                hls.loadSource(url);
                hls.attachMedia(audioPlayer);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {{
                    audioPlayer.play().catch(e => console.log("Autoplay blocked:", e));
                }});
            }} 
            else if (audioPlayer.canPlayType('application/vnd.apple.mpegurl') && url.includes('.m3u8')) {{
                 if (hls) {{ hls.destroy(); hls = null; }}
                 audioPlayer.src = url;
                 audioPlayer.play();
            }}
            else {{
                if (hls) {{ hls.destroy(); hls = null; }}
                audioPlayer.src = url;
                audioPlayer.load(); 
                audioPlayer.play().catch(e => console.log("Autoplay blocked:", e));
            }}
        }}
        function nextStation() {{ currentStationIdx = (currentStationIdx + 1) % stations.length; playStation(currentStationIdx); }}
        function prevStation() {{ currentStationIdx = (currentStationIdx - 1 + stations.length) % stations.length; playStation(currentStationIdx); }}

        // --- 3. 天氣 API (維持不變) ---
        async function fetchWeather() {{
            const city = cityInput.value;
            if(!city) return;
            const url = `https://api.openweathermap.org/data/2.5/weather?q=${{city}}&appid=${{apiKey}}&units=metric&lang=zh_tw`;
            try {{
                const response = await fetch(url);
                if (!response.ok) throw new Error("City not found");
                const data = await response.json();
                wdCity.innerText = data.name; 
                wdTemp.innerText = Math.round(data.main.temp) + "°C";
                wdDesc.innerText = data.weather[0].description;
                const iconCode = data.weather[0].icon;
                wdIcon.src = `https://openweathermap.org/img/wn/${{iconCode}}@2x.png`;
                wdIcon.style.display = "inline-block";
            }} catch (error) {{
                console.error(error);
                wdCity.innerText = "查無此地";
                wdTemp.innerText = "--";
            }}
        }}

        // --- 4. 時間與輪播 (維持不變) ---
        function updateClock() {{
            const now = new window.Date();
            const month = (now.getMonth() + 1).toString().padStart(2, '0');
            const date = now.getDate().toString().padStart(2, '0');
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const seconds = now.getSeconds().toString().padStart(2, '0');
            wdTime.innerText = `${{month}}/${{date}} ${{hours}}:${{minutes}}:${{seconds}}`;
        }}

        setInterval(() => {{
            if (images.length > 0) {{
                currentImgIdx = (currentImgIdx + 1) % images.length;
                slideImg.src = images[currentImgIdx];
            }}
        }}, 5000);

        function toggleRatio() {{
            if (currentRatio === "16/9") currentRatio = "4/3";
            else if (currentRatio === "4/3") currentRatio = "1/1";
            else currentRatio = "16/9";
            frameBox.style.aspectRatio = currentRatio;
            document.getElementById("ratioLabel").innerText = currentRatio.replace("/", ":");
        }}

        function toggleFit() {{
            currentFit = (currentFit === "cover") ? "contain" : "cover";
            slideImg.style.objectFit = currentFit;
            document.getElementById("fitLabel").innerText = currentFit === "cover" ? "Cover (裁切)" : "Contain (完整)";
        }}

        // 啟動
        fetchWeather(); 
        setInterval(updateClock, 1000); 
        updateClock(); 
        playStation(0);
        
        // --- 啟動即時新聞更新 (每 10 分鐘) ---
        fetchLiveNews();
        setInterval(fetchLiveNews, 600000); // 10 minutes

    </script>
</body>
</html>
"""

components.html(html_code, height=820)
