
import streamlit as st

st.title("📻 台灣 FM 廣播 + 圖片輪播")

stations = [
    {"name": "ICRT 國際社區廣播", "iframe": "https://www.radiotaiwan.tw/station/icrt", "audio": "https://live.leanstream.co/ICRTFM-MP3"},
    {"name": "POP Radio", "iframe": "https://popradio.com.tw/player", "audio": "https://stream.popradio.com.tw/popradio.mp3"},
    {"name": "飛碟電台 UFO Radio", "iframe": "https://www.uforadio.com.tw/", "audio": "https://stream.uforadio.com.tw/ufo.mp3"},
    {"name": "News98", "iframe": None, "audio": "https://stream.news98.com.tw/news98.mp3"},
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

if current_station["iframe"]:
    st.markdown(f"""
    {current_station["iframe"]}</iframe>
    """, unsafe_allow_html=True)
else:
