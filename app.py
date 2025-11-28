import streamlit as st
import base64
import json

# 設定頁面寬度，讓 iframe 顯示更完整
st.set_page_config(layout="centered")

st.title("📻 不中斷收音機 & 相框")

# ---------------- 1. Python 處理資料區 (只負責準備資料) ----------------

# 定義電台清單
stations = [
    {"name": "ICRT (英語)", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台 (綜合)", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "港都983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
]

# 上傳照片
uploaded_files = st.file_uploader("📸 上傳相片（建議橫式，最多 10 張）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

img_list = []
if uploaded_files:
    for file in uploaded_files: # 不限張數，有多少傳多少
        b64 = base64.b64encode(file.read()).decode()
        mime_type = file.type
        img_list.append(f"data:{mime_type};base64,{b64}")
else:
    # 預設佔位圖，避免畫面空白
    img_list = ["https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1000&auto=format&fit=crop"]

# 將資料轉換為 JSON 格式傳給 JavaScript
js_stations = json.dumps(stations)
js_images = json.dumps(img_list)

# ---------------- 2. HTML/JS 核心區 (負責所有互動與播放) ----------------
# 我們使用 components.html 或 iframe 的概念，但在這裡用 markdown iframe 技巧
# 這樣可以避免 Streamlit 的按鈕觸發 Rerun

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        font-family: "Helvetica Neue", Arial, sans-serif;
        background-color: #0e1117; /* Streamlit 深色背景 */
        color: white;
        text-align: center;
        margin: 0;
        padding: 10px;
    }}

    /* 相框樣式 */
    .frame-container {{
        width: 100%;
        max-width: 600px;
        margin: 0 auto 20px auto;
        border: 4px solid #333;
        border-radius: 10px;
        background: #000;
        overflow: hidden;
        position: relative;
        transition: aspect-ratio 0.3s ease;
        /* 預設 16/9 */
        aspect-ratio: 16/9; 
    }}

    .frame-img {{
        width: 100%;
        height: 100%;
        object-fit: cover; /* 預設填滿 */
        transition: opacity 1s ease-in-out;
    }}

    /* 控制面板樣式 */
    .controls {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        max-width: 600px;
        margin: auto;
    }}

    .card {{
        background: #262730;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}

    button {{
        background-color: #ff4b4b; /* Streamlit 紅 */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        font-weight: bold;
        width: 100%;
        margin-top: 8px;
        transition: background 0.2s;
    }}
    
    button:hover {{ background-color: #ff2b2b; }}
    button.secondary {{ background-color: #1E90FF; }}
    button.tertiary {{ background-color: #32CD32; }}

    .station-name {{
        font-size: 1.2em;
        font-weight: bold;
        color: #fab005;
        margin-bottom: 5px;
        display: block;
        min-height: 24px;
    }}

    audio {{
        width: 100%;
        margin-top: 10px;
        height: 40px;
    }}
</style>
</head>
<body>

    <div class="frame-container" id="frameBox">
        <img id="slideImg" class="frame-img" src="{img_list[0]}">
    </div>

    <div class="controls">
        <div class="card">
            <div>📻 目前頻道</div>
            <span id="stationLabel" class="station-name">{stations[0]['name']}</span>
            <audio id="audioPlayer" controls autoplay>
                <source id="audioSource" src="{stations[0]['url']}" type="audio/mpeg">
            </audio>
            <button class="secondary" onclick="nextStation()">⏭️ 切換頻道</button>
        </div>

        <div class="card">
            <div>🖼️ 相框設定</div>
            <div style="margin-top:10px; font-size:0.9em; color:#aaa;">狀態：<span id="statusLabel">輪播中</span></div>
            <button class="tertiary" onclick="toggleRatio()">📐 切換比例 (16:9 / 4:3)</button>
            <button onclick="toggleFit()">🔍 切換顯示 (裁切/完整)</button>
        </div>
    </div>

    <script>
        // 接收 Python 傳來的資料
        const stations = {js_stations};
        const images = {js_images};
        
        let currentStationIdx = 0;
        let currentImgIdx = 0;
        let currentRatio = "16/9";
        let currentFit = "cover";

        const audioPlayer = document.getElementById("audioPlayer");
        const audioSource = document.getElementById("audioSource");
        const stationLabel = document.getElementById("stationLabel");
        const slideImg = document.getElementById("slideImg");
        const frameBox = document.getElementById("frameBox");

        // --- 功能 1: 切換電台 (JS 控制，不重整頁面) ---
        function nextStation() {{
            currentStationIdx = (currentStationIdx + 1) % stations.length;
            const station = stations[currentStationIdx];
            
            stationLabel.innerText = station.name;
            
            // 重要：切換音訊來源並播放
            audioPlayer.src = station.url;
            audioPlayer.play().catch(e => console.log("Autoplay blocked:", e));
        }}

        // --- 功能 2: 圖片輪播 ---
        setInterval(() => {{
            if (images.length > 0) {{
                currentImgIdx = (currentImgIdx + 1) % images.length;
                slideImg.src = images[currentImgIdx];
            }}
        }}, 5000); // 每 5 秒

        // --- 功能 3: 切換相框比例 ---
        function toggleRatio() {{
            if (currentRatio === "16/9") {{
                currentRatio = "4/3";
            }} else if (currentRatio === "4/3") {{
                currentRatio = "1/1";
            }} else {{
                currentRatio = "16/9";
            }}
            frameBox.style.aspectRatio = currentRatio;
        }}

        // --- 功能 4: 切換顯示模式 (Cover/Contain) ---
        function toggleFit() {{
            currentFit = (currentFit === "cover") ? "contain" : "cover";
            slideImg.style.objectFit = currentFit;
            
            // 如果是 contain，背景改黑一點以免突兀
            frameBox.style.background = (currentFit === "contain") ? "#000" : "#000"; 
        }}
    </script>
</body>
</html>
"""

# 使用 components.html 渲染，height 設高一點以容納所有內容
import streamlit.components.v1 as components
components.html(html_code, height=650)

st.caption("💡 提示：所有操作皆在前端執行，切換頻道不會造成頁面閃爍或音樂中斷。")
