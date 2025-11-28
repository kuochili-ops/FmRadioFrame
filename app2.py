import streamlit as st
import base64
import json
import streamlit.components.v1 as components
import os

# 設定頁面
st.set_page_config(page_title="Radio & Weather Frame", layout="centered")

st.title("📻 智慧相框收音機 (新增即時新聞跑馬燈)")
st.caption("新聞跑馬燈位於相框下方，不會中斷音樂播放或頁面重載。")

# --- 準備新聞內容 ---
# 這是從 Google Search 取得的即時新聞頭條，將作為跑馬燈內容。
news_snippets = [
    "傅崐萁提修法陸配參政免放棄國籍立院付委審查",
    "總統任命徐斯儉為國防部副部長借重國際戰略長才",
    "新台幣午盤貶1.2分暫收31.352元",
    "財政部：慎防普發一萬釣魚詐騙停止解析11個假網站",
    "黃仁勳談與Google競爭指輝達地位穩固證實已會張忠謀",
    "雲縣推動電動車產業園區設置案已送內政部審議",
    "香港大火死傷慘高樓逃生必知要訣：別找濕毛巾躲浴室",
    "秋季均溫26.5度1951年來最暖氣象署估冬季偏暖雨量略少",
    "傳川普籲高市「別挑釁北京」 日政府否認",
    "禽流感變異成「人傳人」？ 專家示警：比新冠疫情更致命"
]
# 使用 ⭐⭐⭐ 分隔標題
news_ticker_content = " ⭐ 即時新聞 ⭐ ⭐ ⭐ " + " ⭐ ⭐ ⭐ ".join(news_snippets) + " ⭐ ⭐ ⭐ "

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

# 定義預設圖片路徑 (請確保檔案存在 /assets/)
default_image_paths = ["assets/photo1.jpg", "assets/photo2.jpg", "assets/photo3.jpg"] 

# 電台清單
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
        margin: 0 auto 10px auto; /* 留一點空間給跑馬燈 */
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
        background-color: #585d68; /* 跑馬燈底色 */
        color: #fff;
        padding: 5px 0;
        overflow: hidden; /* 隱藏溢出內容 */
        white-space: nowrap; /* 不換行 */
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}

    .news-ticker-content {{
        display: inline-block;
        padding-left: 100%; /* 從右側完全移入 */
        font-weight: 500;
        font-size: 0.9em;
        animation: marquee 60s linear infinite; /* 60s 速度，無限循環 */
    }}

    /* 定義滾動動畫 */
    @keyframes marquee {{
        0% {{ transform: translateX(0%); }}
        100% {{ transform: translateX(-100%); }}
    }}

    /* --- 右下角天氣浮水印 --- */
    .weather-badge {{
        position: absolute;
        bottom: 15px;
        right: 15px;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(4px);
        color: #fff;
        padding: 8px 15px;
        border-radius: 8px;
        z-index: 10;
        font-size: 0.9rem;
    }}

    /* --- 控制面板 --- */
    .controls {{
        display: grid;
        grid-template-columns: 1fr 1fr; 
        gap: 15px;
        max-width: 650px;
        margin: auto;
    }}
    
    .card {{ background: #262730; padding: 15px; border-radius: 8px; border: 1px solid #363940; }}
    .card-title {{ font-size: 0.9rem; color: #bbb; margin-bottom: 8px; font-weight: bold;}}
    .station-name {{ color: #fab005; font-weight: bold; margin-bottom: 5px; display: block; }}
    
    /* === 行動裝置 (Mobile) 優化：資訊在下沿一排 (堆疊) === */
    @media (max-width: 700px) {{
        .frame-container {{ margin-bottom: 10px; }}
        .controls {{ grid-template-columns: 1fr; gap: 10px; }}
        .card {{ padding: 10px; }}
        .card-title {{ display: none; }}
        .input-group {{ flex-direction: column; gap: 5px; }}
        audio {{ height: 30px; }}
        
        /* 縮小並移動天氣浮水印 */
        .weather-badge {{
             bottom: 5px;
             right: 5px;
             padding: 4px 8px;
             font-size: 0.7rem;
        }}
        .weather-temp {{ font-size: 1.2rem; }}
        .weather-desc {{ font-size: 0.7rem; }}
        .time-display {{ font-size: 0.7rem; }}

        /* 手機上讓跑馬燈慢一點 */
        @keyframes marquee {{
            0% {{ transform: translateX(0%); }}
            100% {{ transform: translateX(-100%); }}
        }}
        .news-ticker-content {{ animation: marquee 90s linear infinite; }} /* 變慢 */
    }}

    /* --- 其他樣式維持不變 --- */
    .frame-img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .weather-row {{ display: flex; align-items: center; justify-content: flex-end; gap: 5px; }}
    .weather-temp {{ font-size: 1.4rem; font-weight: bold; color: #fab005; }}
    .weather-city {{ font-size: 0.85rem; font-weight: 600; margin-bottom: 2px; }}
    .weather-desc {{ font-size: 0.8rem; color: #ddd; }}
    .time-display {{ margin-top: 4px; font-size: 0.8rem; color: #ccc; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 4px; }}
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
        <div class="news-ticker-content" id="newsTickerContent">{news_ticker_content}</div>
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
        // JS 邏輯 (維持不變)
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
        
        const wdCity = document.getElementById("wd-city");
        const wdTemp = document.getElementById("wd-temp");
        const wdDesc = document.getElementById("wd-desc");
        const wdIcon = document.getElementById("wd-icon");
        const wdTime = document.getElementById("wd-time");
        const cityInput = document.getElementById("cityInput");

        // --- 1. 音樂播放邏輯 (支援 HLS) ---
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

        function nextStation() {{
            currentStationIdx = (currentStationIdx + 1) % stations.length;
            playStation(currentStationIdx);
        }}

        function prevStation() {{
            currentStationIdx = (currentStationIdx - 1 + stations.length) % stations.length;
            playStation(currentStationIdx);
        }}

        // --- 2. 天氣 API ---
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

        // --- 3. 時間 ---
        function updateClock() {{
            const now = new window.Date();
            const month = (now.getMonth() + 1).toString().padStart(2, '0');
            const date = now.getDate().toString().padStart(2, '0');
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const seconds = now.getSeconds().toString().padStart(2, '0');
            wdTime.innerText = `${{month}}/${{date}} ${{hours}}:${{minutes}}:${{seconds}}`;
        }}

        // --- 4. 圖片輪播 ---
        setInterval(() => {{
            if (images.length > 0) {{
                currentImgIdx = (currentImgIdx + 1) % images.length;
                slideImg.src = images[currentImgIdx];
            }}
        }}, 5000);

        // --- 5. 外觀 ---
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

    </script>
</body>
</html>
"""

components.html(html_code, height=820)
