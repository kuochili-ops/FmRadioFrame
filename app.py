import streamlit as st
import datetime
import requests

# ---------------- 相片輪播 ----------------
uploaded_files = st.file_uploader("📸 上傳相片 (可多選)", type=["jpg","jpeg","png"], accept_multiple_files=True)

if "photo_index" not in st.session_state:
    st.session_state.photo_index = 0

if uploaded_files:
    current_photo = uploaded_files[st.session_state.photo_index]
    st.image(current_photo, caption=f"第 {st.session_state.photo_index+1} 張", use_column_width=True)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ 上一張"):
        st.session_state.photo_index = (st.session_state.photo_index - 1) % len(uploaded_files)
    if col2.button("➡️ 下一張"):
        st.session_state.photo_index = (st.session_state.photo_index + 1) % len(uploaded_files)
else:
    st.info("請先上傳相片")

# ---------------- 電台播放器 ----------------
stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "http://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}
]

if "current_station" not in st.session_state:
    st.session_state.current_station = 0

station = stations[st.session_state.current_station]
st.markdown(f"<h3>🎵 正在播放：{station['name']}</h3>", unsafe_allow_html=True)
st.markdown(f"""
<audio controls autoplay key="{station['url']}">
  <source src="{station['url']}" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)
if col3.button("⬅️ 上一台"):
    st.session_state.current_station = (st.session_state.current_station - 1) % len(stations)
if col4.button("➡️ 下一台"):
    st.session_state.current
