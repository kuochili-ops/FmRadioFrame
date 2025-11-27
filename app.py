import streamlit as st
import datetime
import requests
import pytz
from PIL import Image

# 初始化狀態
if "current_station" not in st.session_state:
    st.session_state.current_station = 0

# ---------------- 上半部：相框 ----------------
uploaded_files = st.file_uploader("📸 上傳相片（最多 5 張）", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded_files:
    photos = uploaded_files[:5]
    slideshow = st.checkbox("▶️ 啟動輪播")
    speed = st.selectbox("⏱️ 輪播速度", ["5 秒", "10 秒", "30 秒"], index=1)
    interval = {"5 秒":5000, "10 秒":10000, "30 秒":30000}[speed]

    # 顯示第一張照片
    st.image(photos[0], use_column_width=True)

    # 台北時間
    tz = pytz.timezone("Asia/Taipei")
    now = datetime.datetime.now(tz)

    # 天氣資訊
    API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
    city = st.text_input("🌍 城市 (例如 Taipei,TW)", "Taipei,TW")
    weather_info = ""
    if API_KEY and city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"
        try:
            res = requests.get(url).json()
            if res.get("cod") == 200:
                temp = res["main"]["temp"]
                desc = res["weather"][0]["description"]
                weather_info = f"{city} {temp}°C {desc}"
        except:
            weather_info = "⚠️ 天氣取得失敗"

    # 疊層資訊 (右下角浮動)
    st.markdown(f"""
    <div style="position:relative; text-align:center;">
      <div style="position:absolute; bottom:20px; right:20px; 
                  background:rgba(0,0,0,0.5); color:white; 
                  padding:10px; border-radius:8px; font-size:16px;">
        🕒 {now.strftime('%H:%M:%S')}<br>
        📅 {now.strftime('%Y-%m-%d')}<br>
        🌤️ {weather_info}
      </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("請上傳相片（最多五張）")

# ---------------- 收音機控制列 ----------------
stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "http://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}
]

station = stations[st.session_state.current_station]

# 播放器置中
st.markdown(f"### 🎶 {station['name']}")
st.markdown(f"""
<div style="text-align:center;">
<audio controls autoplay key="{station['url']}">
  <source src="{station['url']}" type="audio/mpeg">
</audio>
</div>
""", unsafe_allow_html=True)

# 左右箭頭置中
col_left, col_center, col_right = st.columns([1,2,1])
with col_left:
    if st.button("⬅️"):
        st.session_state.current_station = (st.session_state.current_station - 1) % len(stations)
with col_right:
    if st.button("➡️"):
        st.session_state.current_station = (st.session_state.current_station + 1) % len(stations)
