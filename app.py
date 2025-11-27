import streamlit as st
import datetime
import requests
import pytz
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# ---------------- 初始化狀態 ----------------
if "photo_index" not in st.session_state:
    st.session_state.photo_index = 0
if "current_station" not in st.session_state:
    st.session_state.current_station = 0
if "slideshow" not in st.session_state:
    st.session_state.slideshow = False
if "radio_container" not in st.session_state:
    st.session_state.radio_container = st.empty()

# ---------------- 自動刷新（照片輪播） ----------------
if st.session_state.slideshow:
    st_autorefresh(interval=5000, key="slideshow_refresh")

# ---------------- 相框區 ----------------
uploaded_files = st.file_uploader("📸 上傳相片（最多 5 張）", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded_files:
    photos = uploaded_files[:5]

    current_photo = photos[st.session_state.photo_index]
    img = Image.open(current_photo)
    st.image(img, use_column_width=True)

    if st.session_state.slideshow:
        st.session_state.photo_index = (st.session_state.photo_index + 1) % len(photos)

    tz = pytz.timezone("Asia/Taipei")
    now = datetime.datetime.now(tz)

    API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
    city = "Taipei,TW"
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

# ---------------- 收音機區 ----------------
stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
]

station = stations[st.session_state.current_station]

# 頻道名稱（小字 + 白字 + 半透明黑底）
st.markdown(f"""
<div style="text-align:center; margin-top:10px;">
  <span style="background:rgba(0,0,0,0.5); 
               color:white; 
               padding:6px 12px; 
               border-radius:6px; 
               font-size:16px; 
               font-weight:bold;">
    🎶 {station['name']}
  </span>
</div>
""", unsafe_allow_html=True)

# 播放器容器（覆蓋舊的，避免多重播放）
st.session_state.radio_container.markdown(f"""
<div style="text-align:center; margin-top:10px;">
<audio controls autoplay>
  <source src="{station['url']}" type="audio/mpeg">
</audio>
</div>
""", unsafe_allow_html=True)

# ---------------- 控制列（左右排列 + 狀態底色 + 狀態提示） ----------------
col_left, col_right = st.columns([1,1])

# 頻道切換：固定藍色
with col_left:
    st.markdown("""
    <style>
    div[data-testid="channel_switch"] button {
        background-color: #1E90FF; /* 藍色 */
        color: white;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("📻 頻道切換", key="channel_switch"):
        st.session_state.current_station = (st.session_state.current_station + 1) % len(stations)
    st.caption(f"目前頻道：{stations[st.session_state.current_station]['name']}")

# 照片輪播：依狀態變色（綠色/灰色）
slideshow_color = "#32CD32" if st.session_state.slideshow else "#808080"
slideshow_status = "輪播中" if st.session_state.slideshow else "已停止"

with col_right:
    st.markdown(f"""
    <style>
    div[data-testid="photo_toggle"] button {{
        background-color: {slideshow_color};
        color: white;
        font-weight: bold;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)
    if st.button("🖼️ 照片輪播", key="photo_toggle"):
        st.session_state.slideshow = not st.session_state.slideshow
    st.caption(f"狀態：{slideshow_status}")
