
import streamlit as st

# 設定頁面
st.set_page_config(page_title="台灣 FM 廣播選台", layout="centered")
st.title("📻 台灣 FM 廣播選台")

# 廣播串流清單
stations = [
    {"name": "ICRT 國際社區廣播", "url": "https://live.leanstream.co/ICRTFM-MP3"},
    {"name": "HitFM 北部", "url": "https://hichannel.hinet.net/radio/HitFM"},
    {"name": "中廣音樂網 iRadio", "url": "https://hichannel.hinet.net/radio/iRadio"},
    {"name": "飛揚調頻 FM89.5", "url": "http://asiafm.rastream.com/asiafm-fly"},
    {"name": "大愛網路電台", "url": "http://radiolive.newdaai.tv:8020"},
    {"name": "寶島新聲 FM98.5", "url": "http://stream.superfm99-1.com.tw:8555/"},
    {"name": "大千電台 FM99.1", "url": "http://stream.superfm99-1.com.tw:8554/"},
]

# 初始化選台索引
if "index" not in st.session_state:
    st.session_state.index = 0

# 左右鍵選台
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅ 上一台"):
        st.session_state.index = (st.session_state.index - 1) % len(stations)
with col2:
    if st.button("下一台 ➡"):
        st.session_state.index = (st.session_state.index + 1) % len(stations)

# 顯示目前選台
current_station = stations[st.session_state.index]
st.subheader(f"🎶 現在播放：{current_station['name']}")

# 播放音訊（HTML audio，避免 HTTP/HTTPS 混合問題）
st.markdown(f"""
<audio controls autoplay style="width:100%">
  <source src="{current_station['url']}" type="audio/mpeg">
  您的瀏覽器不支援音訊播放。
</audio>
""", unsafe_allow_html=True)
