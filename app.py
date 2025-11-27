
import streamlit as st
import time

# 頁面設定
st.set_page_config(page_title="FM 廣播 + 圖片輪播", layout="centered")

st.title("📻 FM 廣播 + 相片輪播 (Streamlit Cloud 版本)")

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

# --- 廣播選台 (固定 MP3 播放清單) ---
st.subheader("FM 廣播選台 (MP3 播放清單)")
stations = [
    {"name": "音樂台 1", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
    {"name": "音樂台 2", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
    {"name": "音樂台 3", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"}
]  # ← 注意這裡要有結尾的 ]

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
