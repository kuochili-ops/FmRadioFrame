import streamlit as st
import base64
import json
import streamlit.components.v1 as components

# 設定頁面
st.set_page_config(page_title="Radio & Weather Frame", layout="centered")

st.title("📻 智慧相框收音機 (六頻道版)")
st.caption("整合 OpenWeatherMap、HLS 串流支援、不中斷播放")

# ---------------- 1. Python 資料準備區 ----------------

# 更新後的電台清單
stations = [
    {"name": "ICRT (英語)", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台 (綜合)", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事 989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都 983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "https://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}, # 已轉為 https 以防被擋
]

# 上傳照片
uploaded_files = st.file_uploader("📸 上傳相片（建議橫式，無上限）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

img_list = []
if uploaded_files:
    for file in uploaded_files:
        b64 = base64.b64encode(file.read()).decode()
        mime_type = file.type
        img_list.append(f"data:{mime_type};base64,{b64}")
else:
    # 預設風景圖
    img_list = [
        "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    ]

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
        margin: 0 auto 20px auto;
        border: 4px solid #333;
        border-radius: 12px;
        background: #000;
        overflow: hidden;
        position: relative;
        transition: aspect-ratio 0.3s ease;
        aspect-ratio: 16/9;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }}

    .frame-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: opacity 1s ease-in-out;
        display: block;
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
        text-align: right;
        min-width: 120px;
        z-index: 10;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.1);
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }}

    .weather-row {{ display: flex; align-items: center; justify-content: flex-end; gap: 5px; }}
    .weather-temp {{ font-size: 1.4rem; font-weight: bold; color: #fab005; }}
    .weather-city {{ font-size: 0.85rem; font-weight: 600; margin-bottom: 2px; }}
    .weather-desc {{ font-size: 0.8rem; color: #ddd; }}
    .time-display {{ margin-top: 4px; font-size: 0.8rem; color: #ccc; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 4px; }}
    
    /* --- 控制面板 --- */
    .controls {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        max-width: 650px;
        margin: auto;
    }}

    .card {{
        background: #262730;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #363940;
    }}
    
    .card-title {{ font-size: 0.9rem; color: #bbb; margin-bottom: 8px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;}}

    button {{
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        width: 100%;
        margin-top: 5px;
        transition: 0.2s;
    }}
    button:hover {{ opacity: 0.9; }}
    button.btn-blue {{ background-color: #1E90FF; }}
    button.btn-green {{ background-color: #32CD32; }}
    button.btn-gray {{ background-color: #555; margin-top:0; width: auto; font-size: 12px; }}

    input[type="text"] {{
        width: 60%;
        padding: 6px;
        border-radius: 4px;
        border: 1px solid #555;
        background: #111;
        color: white;
    }}

    .input-group {{ display: flex; gap: 5px; margin-bottom: 10px; }}

    audio {{ width: 100%; height: 35px; margin-top: 8px; }}
    .station-name {{ color: #fab005; font-weight: bold; margin-bottom: 5px; display: block; }}

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

    <div class="controls">
        <div class="card">
            <div class="card-title">🌦️ 城市 & 音樂</div>
            
            <div class="input-group">
                <input type="text" id="cityInput" value="Taipei, Taiwan" placeholder="Enter City">
                <button class="btn-gray" onclick="fetchWeather()">更新</button>
            </div>

            <div style="border-top: 1px solid #444; margin: 10px 0;"></div>

            <span id="stationLabel" class="station-name">{stations[0]['name']}</span>
            <audio id="audioPlayer" controls>
                </audio>
            
            <div style="display:flex; gap:5px; margin-top:5px;">
                <button class="btn-blue" onclick="prevStation()">⏮️</button>
                <button class="btn-blue" onclick="nextStation()">⏭️ 下一頻道</button>
            </div>
        </div>

        <div class="card">
            <div class="card-title">🖼️ 相框控制</div>
            <div style="margin-bottom:10px; font-size:0.85em; color:#aaa;">
                目前顯示：<span id="fitLabel">Cover (裁切)</span><br>
                目前比例：<span id="ratioLabel">16:9</span>
            </div>
            <button class="btn-green" onclick="toggleRatio()">📐 切換比例</button>
            <button onclick="toggleFit()">🔍 切換顯示</button>
        </div>
    </div>

    <script>
        // 資料初始化
        const stations = {js_stations};
        const images = {js_images};
        const apiKey = "{api_key}";

        let currentStationIdx = 0;
        let currentImgIdx = 0;
        let currentRatio = "16/9";
        let currentFit = "cover";
        let hls = null; // HLS 實例

        // DOM 元素
        const audioPlayer = document.getElementById("audioPlayer");
        const stationLabel = document.getElementById("stationLabel");
        const slideImg = document.getElementById("slideImg");
        const frameBox = document.getElementById("frameBox");
        
        // 天氣 DOM
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

            // 檢查是否支援 HLS (針對 m3u8)
            if (Hls.isSupported() && url.includes('.m3u8')) {{
                if (hls) {{
                    hls.destroy();
                }}
                hls = new Hls();
                hls.loadSource(url);
                hls.attachMedia(audioPlayer);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {{
                    audioPlayer.play().catch(e => console.log("Autoplay blocked:", e));
                }});
            }} 
            // 針對 Safari (原生支援 m3u8) 或一般 MP3
            else if (audioPlayer.canPlayType('application/vnd.apple.mpegurl') && url.includes('.m3u8')) {{
                 if (hls) {{ hls.destroy(); hls = null; }}
                 audioPlayer.src = url;
                 audioPlayer.play();
            }}
            else {{
                // 一般 MP3 串流
                if (hls) {{ hls.destroy(); hls = null; }}
                audioPlayer.src = url;
                audioPlayer.load(); // 重新載入
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
        // 頁面載入時先準備好播放器 (但不一定自動播放，視瀏覽器政策)
        playStation(0);

    </script>
</body>
</html>
"""

# 使用 components 渲染
components.html(html_code, height=800)
