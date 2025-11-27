
import streamlit as st
import time

# 頁面設定
st.set_page_config(page_title="台灣 FM 廣播 + 圖片輪播", layout="centered")

st.title("📻 台灣 FM 廣播 + 相片輪播")

# --- 圖片輪播 ---
st.subheader("相片輪播")
sample_photos = ["assets/photo1.jpg", "assets/photo2.jpg", "assets/photo3.jpg"]

if "photo_index" not in st.session_state:
    st.session_state.photo_index = 0

img_placeholder = st.empty()
img_placeholder.image(sample_photos[st.session_state.photo_index], use_column_width=True)

def auto_slide():
    for _ in range(10):  # 播放 10 次循環
        time.sleep(5)
        st.session_state.photo_index = (st.session_state.photo_index + 1) % len(sample_photos)
        img_placeholder.image(sample_photos[st.session_state.photo_index], use_column_width=True)

if st.button("開始輪播"):
    auto_slide()

# --- 廣播選台 ---
st.subheader("FM 廣播選台")
stations = [
    {"name": "ICRT 國際社區廣播", "iframe": "https://www.radiotaiwan.tw/station/icrt"},
    {"name": "POP Radio", "iframe": "https://popradio.com.tw/player"},
    {"name": "飛碟電台 UFO Radio", "iframe": "https://www.uforadio.com.tw/"},
    {"name": "News98", "iframe": "https://www.news98.com.tw/"},
]

if "station_index" not in st.session_state:
    st.session_state.station_index = 0

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅ 上一台"):
        st.session_state.station_index = (st.session_state.station_index - 1) % len(stations)
with col2:
    if st.button("下一台 ➡"):
        st.session_state.station_index = (st.session_state.station_index + 1) % len(stations)

current_station = stations[st.session_state.station_index]
st.subheader(f"🎶 現在播放：{current_station['name']}")

# 嵌入官方播放器 iframe
st.markdown(f"""
<iframe src="{current_station['iframe']}" width="100%" height="500" frameborder="0" allow="autoplay"></iframe>
""", unsafe_allow_html=True)
