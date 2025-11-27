import streamlit as st
import datetime
import requests
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# 初始化狀態
if "photo_index" not in st.session_state:
    st.session_state.photo_index = 0
if "current_station" not in st.session_state:
    st.session_state.current_station = 0
if "slideshow" not in st.session_state:
    st.session_state.slideshow = False

# 自動刷新（每 30 秒）
st_autorefresh(interval=30 * 1000, key="refresh")

# ---------------- 上半部：相框 ----------------
uploaded_files = st.file_uploader("📸 上傳相片（最多 5 張）", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded_files:
    photos = uploaded_files[:5]
    st.session_state.slideshow = st.checkbox("▶️ 啟動輪播")

    current_photo = photos[st.session_state.photo_index]
    img = Image.open(current_photo)

    # 判斷橫式或直式
    if img.width >= img.height:
        st.image(img, use_column_width=True)
    else:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st.image(img, width=400)
        st.markdown("</div>", unsafe_allow_html=True)

    # 自動輪播
    if st.session_state.slideshow:
        st.session_state.photo_index = (st.session_state.photo_index + 1) % len(photos)
else:
    st.info("請上傳相片（最多五張）")

# ---------------- 下半部：收音機與資訊 ----------------
stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "http://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}
]

station = stations[st.session_state.current_station]
st.markdown(f"### 🎶 正在播放：{station['name']}")
st.markdown(f"""
<audio controls autoplay key="{station['url']}">
  <source src="{station['url']}" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

col3, col4 = st.columns([1,1])
if col3.button("⬅️ 上一台"):
    st.session_state.current_station = (st.session_state.current_station - 1) % len(stations)
if col4.button("➡️ 下一台"):
    st.session_state.current_station = (st.session_state.current_station + 1) % len(stations)

# ---------------- 下半部資訊 ----------------
now = datetime.datetime.now()
st.markdown(f"🕒 時間：{now.strftime('%H:%M:%S')}")
st.markdown(f"📅 日期：{now.strftime('%Y-%m-%d')}")

API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
city = st.text_input("🌍 城市 (例如 Taipei,TW)", "Taipei,TW")

if API_KEY and city:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"
    try:
        res = requests.get(url).json()
        if res.get("cod") == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            st.markdown(f"🌤️ {city}：{temp}°C，{desc}")
        else:
            st.warning(f"⚠️ API 錯誤：{res.get('message')}")
    except Exception as e:
        st.error(f"⚠️ 無法取得天氣資訊：{e}")
