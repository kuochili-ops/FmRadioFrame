
import streamlit as st

st.title("🎵 台灣 FM 廣播選台")
stations = [
    {"name": "ICRT 國際社區廣播", "url": "https://live.leanstream.co/ICRTFM-MP3"},
    {"name": "POP Radio", "url": "https://stream.popradio.com.tw/popradio.mp3"},
    {"name": "飛碟電台 UFO Radio", "url": "https://stream.uforadio.com.tw/ufo.mp3"},
    {"name": "News98", "url": "https://stream.news98.com.tw/news98.mp3"},
]

if "index" not in st.session_state:
    st.session_state.index = 0

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅ 上一台"):
        st.session_state.index = (st.session_state.index - 1) % len(stations)
with col2:
    if st.button("下一台 ➡"):
        st.session_state.index = (st.session_state.index + 1) % len(stations)

current_station = stations[st.session_state.index]
st.subheader(f"🎶 現在播放：{current_station['name']}")
st.audio(current_station["url"], format="audio/mp3")
